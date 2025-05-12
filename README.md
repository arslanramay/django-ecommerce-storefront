# Storefront Project - Technical Documentation

This document serves as the technical documentation for the **Storefront** project. It provides an overview of the features implemented, along with details of the files changed and links to related commits. This documentation is designed to help track the progress of the project and serve as a reference for future development.

---

## Table of Contents
1. [Overview](#overview)
2. [Features Implemented](#features-implemented)
   - [Orders API](#orders-api)
   - [Cart Management](#cart-management)
   - [Product Management](#product-management)
   - [Customer Management](#customer-management)
   - [Authentication and Authorization](#authentication-and-authorization)
   - [Reviews API](#reviews-api)
   - [Debug Toolbar Integration](#debug-toolbar-integration)
3. [Database Schema](#database-schema)
4. [REST API Endpoints](#rest-api-endpoints)

---

## Overview

The **Storefront** project is a Django-based e-commerce platform that provides APIs for managing products, orders, customers, and more. It uses Django REST Framework (DRF) for building APIs and integrates with third-party libraries like Djoser for authentication.

---

## Features Implemented

### 1. Orders API
**Description:**  
The Orders API allows customers to place orders, view their order history, and manage order items.

**Key Changes:**
- Added `Order` and `OrderItem` models in [`store/models.py`](store/models.py).
- Created serializers for orders:
  - [`OrderSerializer`](store/serializers.py)
  - [`CreateOrderSerializer`](store/serializers.py)
- Implemented order creation logic in `CreateOrderSerializer.save()`:
  - Handles cart-to-order conversion.
  - Deletes the cart after order creation.
- Added permissions for canceling orders in [`store/migrations/0011_alter_order_options.py`](store/migrations/0011_alter_order_options.py).

**Files Changed:**
- [`store/models.py`](store/models.py)
- [`store/serializers.py`](store/serializers.py)
- [`store/migrations/`](store/migrations/)

**Related Commits:**
- [Add Order and OrderItem models](#)
- [Implement CreateOrderSerializer](#)
- [Add permissions for canceling orders](#)

---

### 2. Cart Management
**Description:**  
The Cart Management feature allows customers to add, update, and remove items from their shopping cart.

**Key Changes:**
- Added `Cart` and `CartItem` models in [`store/models.py`](store/models.py).
- Created serializers for cart operations:
  - [`AddCartItemSerializer`](store/serializers.py)
  - [`UpdateCartItemSerializer`](store/serializers.py)
  - [`CartItemSerializer`](store/serializers.py)
- Implemented logic for adding items to the cart in `AddCartItemSerializer.save()`.

**Files Changed:**
- [`store/models.py`](store/models.py)
- [`store/serializers.py`](store/serializers.py)
- [`store/migrations/`](store/migrations/)

**Related Commits:**
- [Add Cart and CartItem models](#)
- [Implement AddCartItemSerializer](#)

---

### 3. Product Management
**Description:**  
The Product Management feature provides APIs for listing, creating, updating, and deleting products.

**Key Changes:**
- Added `Product` and `Collection` models in [`store/models.py`](store/models.py).
- Created `ProductSerializer` in [`store/serializers.py`](store/serializers.py).
- Implemented tax calculation logic in `ProductSerializer.calculate_tax()`.

**Files Changed:**
- [`store/models.py`](store/models.py)
- [`store/serializers.py`](store/serializers.py)
- [`store/views.py`](store/views.py)

**Related Commits:**
- [Add Product and Collection models](#)
- [Implement ProductSerializer](#)

---

### 4. Customer Management
**Description:**  
The Customer Management feature allows managing customer profiles and their associated data.

**Key Changes:**
- Added `Customer` model in [`store/models.py`](store/models.py).
- Created `CustomerSerializer` in [`store/serializers.py`](store/serializers.py).
- Linked customers to users via a `OneToOneField`.

**Files Changed:**
- [`store/models.py`](store/models.py)
- [`store/serializers.py`](store/serializers.py)

**Related Commits:**
- [Add Customer model](#)
- [Implement CustomerSerializer](#)

---

### 5. Authentication and Authorization
**Description:**  
Integrated authentication and authorization using Djoser and JWT.

**Key Changes:**
- Configured `SIMPLE_JWT` in [`storefront/settings.py`](storefront/settings.py).
- Customized Djoser serializers for user creation and management.

**Files Changed:**
- [`storefront/settings.py`](storefront/settings.py)

**Related Commits:**
- [Integrate Djoser for authentication](#)
- [Configure JWT authentication](#)

---

### 6. Reviews API
**Description:**  
The Reviews API allows customers to leave reviews for products.

**Key Changes:**
- Added `Review` model in [`store/models.py`](store/models.py).
- Created `ReviewSerializer` in [`store/serializers.py`](store/serializers.py).
- Implemented review creation logic in `ReviewSerializer.create()`.

**Files Changed:**
- [`store/models.py`](store/models.py)
- [`store/serializers.py`](store/serializers.py)

**Related Commits:**
- [Add Review model](#)
- [Implement ReviewSerializer](#)

---

### 7. Debug Toolbar Integration
**Description:**  
Integrated Django Debug Toolbar for performance monitoring and debugging.

**Key Changes:**
- Added `debug_toolbar` to `INSTALLED_APPS` in [`storefront/settings.py`](storefront/settings.py).
- Configured middleware and URLs for Debug Toolbar.

**Files Changed:**
- [`storefront/settings.py`](storefront/settings.py)
- [`storefront/urls.py`](storefront/urls.py)

**Related Commits:**
- [Integrate Django Debug Toolbar](#)

---

## Database Schema
The database schema includes the following key models:
- `Product`
- `Collection`
- `Customer`
- `Order`
- `OrderItem`
- `Cart`
- `CartItem`
- `Review`

Refer to the migrations folder for detailed schema changes: [`store/migrations/`](store/migrations/).

---

## REST API Endpoints
Here are some of the key API endpoints implemented:

### Products
- `GET /store/products/` - List all products.
- `POST /store/products/` - Create a new product.

### Orders
- `POST /store/orders/` - Create a new order.
- `GET /store/orders/` - List all orders for the authenticated user.

### Cart
- `POST /store/cart/items/` - Add an item to the cart.
- `PATCH /store/cart/items/<id>/` - Update the quantity of a cart item.

### Reviews
- `POST /store/products/<id>/reviews/` - Add a review for a product.

---

This documentation will be updated as new features are implemented.
