document.addEventListener('DOMContentLoaded', function() {
    console.log('Cart JS loaded');  // Debug log
    
    // Add to cart button click handler
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();  // Prevent any default action
            const productName = this.dataset.productName;
            console.log('Adding to cart:', productName);  // Debug log
            addToCart(productName);
        });
    });

    // Load cart if user is logged in
    if (document.querySelector('.cart-count')) {
        loadCart();
    }
});

function addToCart(productName) {
    console.log('Making fetch request for:', productName);  // Debug log
    
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product_name: productName
        })
    })
    .then(response => {
        console.log('Response received:', response);  // Debug log
        return response.json();
    })
    .then(data => {
        console.log('Data received:', data);  // Debug log
        if (data.success) {
            loadCart();  // Refresh cart display
            alert('Added to cart!');
        } else {
            alert(data.message || 'Failed to add to cart');
        }
    })
    .catch(error => {
        console.error('Error:', error);  // Debug log
        alert('Error adding to cart');
    });
}

function loadCart() {
    fetch('/api/cart/')
        .then(response => response.json())
        .then(data => {
            // Update cart count
            document.querySelector('.cart-count').textContent = data.total_items || '0';
            
            // Update cart items if dropdown is present
            const cartItems = document.querySelector('.cart-items');
            if (cartItems) {
                if (data.items && data.items.length > 0) {
                    cartItems.innerHTML = data.items.map(item => `
                        <div class="cart-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-0">${item.product_name}</h6>
                                    <small class="text-muted">$${item.price} x ${item.quantity}</small>
                                </div>
                                <div class="btn-group btn-group-sm">
                                    <button class="btn btn-outline-secondary" onclick="updateQuantity('${item.product_name}', -1)">-</button>
                                    <button class="btn btn-outline-secondary" onclick="updateQuantity('${item.product_name}', 1)">+</button>
                                </div>
                            </div>
                        </div>
                    `).join('');
                } else {
                    cartItems.innerHTML = '<div class="cart-empty">Your cart is empty</div>';
                }
                
                document.querySelector('.cart-total').textContent = data.total_price || '0.00';
            }
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateQuantity(productName, change) {
    fetch('/api/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product_name: productName,
            change: change
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadCart();  // Refresh cart display
        } else {
            alert(data.message || 'Failed to update quantity');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating quantity');
    });
} 