from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, ignore_result=True)
def log_new_product_task(self, product_name, product_id, category_name, price):
    """
    Background task to log information about a new product being added.

    Args:
        product_name (str): Name of the new product
        product_id (int): ID of the new product
        category_name (str): Name of the product's category
        price (str): Price of the product
    """
    try:
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"[{timestamp}] NEW PRODUCT ADDED:\n"
            f"  - Name: {product_name}\n"
            f"  - ID: {product_id}\n"
            f"  - Category: {category_name}\n"
            f"  - Price: ${price}\n"
            f"  - Task ID: {self.request.id}\n"
            f"{'='*50}"
        )
        print(message)
        logger.info(f"New product added: {product_name} (ID: {product_id})")
        return f"Successfully logged new product: {product_name}"

    except Exception as exc:
        logger.error(f"Error in log_new_product_task: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)
