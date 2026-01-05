#!/bin/bash

# Move to project root (IMPORTANT for manage.py)
cd /home/pheonix/Developments/alx-backend-graphql_crm || exit 1

# Run Django shell command and capture deleted count
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

qs = Customer.objects.filter(
    orders__isnull=True
) | Customer.objects.filter(
    orders__created_at__lt=one_year_ago
)

deleted_count, _ = qs.distinct().delete()
print(deleted_count)
")

# Log result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
