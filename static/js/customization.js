const MIN_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.minServings || 1);
const MAX_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.maxServings || 12);
const DEFAULT_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.defaultServings || 2);
const BASE_PRICE = parseFloat(document.querySelector('[name="recipe"]')?.dataset?.basePrice || 0);

// Initialize price on page load
document.addEventListener('DOMContentLoaded', function() {
    updatePrice();
});

function decreaseServings() {
    const input = document.getElementById('servings-input');
    const current = parseInt(input.value);
    if (current > MIN_SERVINGS) {
        input.value = current - 1;
        updatePrice();
    }
}

function increaseServings() {
    const input = document.getElementById('servings-input');
    const current = parseInt(input.value);
    if (current < MAX_SERVINGS) {
        input.value = current + 1;
        updatePrice();
    }
}

function updatePrice() {
    const servings = parseInt(document.getElementById('servings-input').value);
    const checkboxes = document.querySelectorAll('.ingredient-checkbox:checked');
    
    // Calculate servings multiplier
    const servingsMultiplier = servings / DEFAULT_SERVINGS;
    
    // Calculate original price for servings
    const originalPrice = BASE_PRICE * servingsMultiplier;
    document.getElementById('original-price').textContent = originalPrice.toFixed(2);
    
    // Calculate savings from excluded ingredients
    let excludedSavings = 0;
    let excludedIngredientIds = [];
    
    checkboxes.forEach(checkbox => {
        // You'll need to pass ingredient prices from the server
        // For now, we'll calculate on the server side
        excludedIngredientIds.push(checkbox.value);
    });
    
    // Call server to calculate exact savings
    if (excludedIngredientIds.length > 0) {
        fetch(window.RECIPES_CALCULATE_PRICE_URL || '/calculate-price/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({
                recipe_id: document.querySelector('[name="recipe"]')?.value,
                servings: servings,
                excluded_ingredients: excludedIngredientIds
            })
        })
        .then(response => response.json())
        .then(data => {
            excludedSavings = data.savings;
            updatePriceDisplay(originalPrice, excludedSavings, servingsMultiplier);
        });
    } else {
        updatePriceDisplay(originalPrice, 0, servingsMultiplier);
    }
    
    // Store excluded ingredients for form submission
    document.getElementById('excluded-ingredients-field').value = excludedIngredientIds.join(',');
    
    // Update servings field for form submission
    document.getElementById('servings-field').value = servings;
}

function updatePriceDisplay(originalPrice, savings, multiplier) {
    const finalPrice = Math.max(originalPrice - savings, 0.01);
    
    // Update price display
    document.getElementById('final-price').textContent = finalPrice.toFixed(2);
    
    // Show/hide savings section
    const savingsSection = document.getElementById('excluded-savings');
    if (savings > 0) {
        savingsSection.style.display = 'flex';
        document.getElementById('excluded-savings-amount').textContent = savings.toFixed(2);
    } else {
        savingsSection.style.display = 'none';
    }
    
    // Show/hide servings adjustment
    if (multiplier !== 1.0) {
        document.getElementById('servings-adjustment').style.display = 'flex';
        document.getElementById('servings-adjustment-amount').textContent = '×' + multiplier.toFixed(1);
    } else {
        document.getElementById('servings-adjustment').style.display = 'none';
    }
}

function saveLater() {
    alert('Save for Later feature coming soon!');
    // TODO: Implement saved recipes functionality
}


