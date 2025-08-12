#!/bin/bash
# Script to substitute environment variables in asm3.conf template

# Read the template and substitute environment variables
envsubst < /app/asm3.conf.template > /etc/asm3.conf

echo "Configuration file generated with environment variables:"
echo "SMTP Host: $ASM3_SMTP_HOST"
echo "SMTP Port: $ASM3_SMTP_PORT"
echo "From Address: $ASM3_FROM_ADDRESS"
echo "Use Sendmail: $ASM3_USE_SENDMAIL"