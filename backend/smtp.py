from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
import os
import django
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file
from django.utils.html import strip_tags
# Emails = User.objects.filter(role="buyer").values_list("email", flat=True)

product = {
    "name": "Fresh Wheat Seeds",
    "price": "₹499",
    "image": "https://yourdomain.com/media/products/wheat.jpg",
    "description": "High quality seeds for better yield."
}

subject = "🌱 New Product Added - AgroMart"
from_email = os.getenv('EMAIL_HOST_USER')

html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      padding: 20px;
    }}
    .container {{
      max-width: 600px;
      background: #ffffff;
      padding: 20px;
      border-radius: 10px;
      margin: auto;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .product-img {{
      width: 100%;
      border-radius: 10px;
    }}
    .title {{
      font-size: 24px;
      font-weight: bold;
      margin-top: 15px;
    }}
    .price {{
      color: green;
      font-size: 20px;
      margin: 10px 0;
    }}
    .btn {{
      display: inline-block;
      padding: 10px 15px;
      background: #28a745;
      color: white;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 10px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <img src="{product['image']}" class="product-img" />
    <div class="title">{product['name']}</div>
    <div class="price">{product['price']}</div>
    <p>{product['description']}</p>
    <a href="https://yourdomain.com/products" class="btn">View Product</a>
  </div>
</body>
</html>
"""
plain_message = strip_tags(html_content)
Emails = ["patidardevkaran2@gmail.com"]

send_mail(
        plain_message,
        from_email,
        list([Emails]),
        html_message=html_content
        fail_silently=False,
    )