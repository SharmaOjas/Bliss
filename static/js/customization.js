const MIN_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.minServings || document.querySelector('[name="recipe"]')?.dataset?.minServings || 1);
const MAX_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.maxServings || document.querySelector('[name="recipe"]')?.dataset?.maxServings || 12);
const DEFAULT_SERVINGS = parseInt(document.querySelector('[name="recipe"]')?.dataset?.defaultServings || document.querySelector('[name="recipe"]')?.dataset?.defaultServings || 2);
const BASE_PRICE = (() => {
  const el = document.querySelector('[name="recipe"]');
  const ds = el?.dataset;
  // Support dashed data-* mapping (data-base-price => dataset.basePrice)
  const dsVal = ds?.basePrice ? parseFloat(ds.basePrice) : NaN;
  if (!isNaN(dsVal)) return dsVal;
  const domVal = parseFloat(document.getElementById('original-price')?.textContent || document.getElementById('final-price')?.textContent || '0');
  return isNaN(domVal) ? 0 : domVal;
})();

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
    let servings = parseInt(document.getElementById('servings-input').value, 10);
    if (Number.isNaN(servings)) servings = DEFAULT_SERVINGS;
    // Clamp to min/max
    servings = Math.min(Math.max(servings, MIN_SERVINGS), MAX_SERVINGS);
    // Update per-ingredient quantities and prices for current servings
    updateIngredientPrices(servings);
    const checkboxes = document.querySelectorAll('.ingredient-checkbox:checked');
    
    // Calculate servings multiplier
    let servingsMultiplier = servings / DEFAULT_SERVINGS;
    if (!Number.isFinite(servingsMultiplier) || Number.isNaN(servingsMultiplier)) {
        servingsMultiplier = 1.0;
    }
    
    // Calculate original price for servings
    let originalPrice = BASE_PRICE * servingsMultiplier;
    if (!Number.isFinite(originalPrice) || Number.isNaN(originalPrice)) {
        originalPrice = BASE_PRICE;
    }
    const originalEl = document.getElementById('original-price');
    if (originalEl) originalEl.textContent = originalPrice.toFixed(2);
    
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
                recipe_slug: document.querySelector('[name="recipe"]')?.value,
                servings: servings,
                excluded_ingredients: excludedIngredientIds
            })
        })
        .then(response => response.json())
        .then(data => {
            const savings = parseFloat(data?.savings);
            excludedSavings = Number.isNaN(savings) ? 0 : savings;
            updatePriceDisplay(originalPrice, excludedSavings, servingsMultiplier);
        })
        .catch(() => {
            updatePriceDisplay(originalPrice, 0, servingsMultiplier);
        });
    } else {
        updatePriceDisplay(originalPrice, 0, servingsMultiplier);
    }
    
    // Store excluded ingredients for form submission as repeated inputs
    const container = document.getElementById('excluded-inputs-container');
    if (container) {
        container.innerHTML = '';
        excludedIngredientIds.forEach(id => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'excluded_ingredients';
            input.value = id;
            container.appendChild(input);
        });
    }
    
    // Update servings field for form submission
    document.getElementById('servings-field').value = servings;
}

function updatePriceDisplay(originalPrice, savings, multiplier) {
    const base = Number.isFinite(originalPrice) ? originalPrice : 0;
    const save = Number.isFinite(savings) ? savings : 0;
    const finalPrice = Math.max(base - save, 0.00);
    
    // Update price display
    const finalEl = document.getElementById('final-price');
    if (finalEl) finalEl.textContent = finalPrice.toFixed(2);
    
    // Show/hide savings section
    const savingsSection = document.getElementById('excluded-savings');
    if (save > 0) {
        savingsSection.style.display = 'flex';
        const saveEl = document.getElementById('excluded-savings-amount');
        if (saveEl) saveEl.textContent = save.toFixed(2);
    } else {
        savingsSection.style.display = 'none';
    }
    
    // Show/hide servings adjustment
    if (Number.isFinite(multiplier) && multiplier !== 1.0) {
        const adj = document.getElementById('servings-adjustment');
        const adjAmt = document.getElementById('servings-adjustment-amount');
        if (adj) adj.style.display = 'flex';
        if (adjAmt) adjAmt.textContent = '×' + multiplier.toFixed(1);
    } else {
        const adj = document.getElementById('servings-adjustment');
        if (adj) adj.style.display = 'none';
    }
}

function updateIngredientPrices(servings) {
    const defaultServings = DEFAULT_SERVINGS || 1;
    const items = document.querySelectorAll('.ingredient-item');
    items.forEach(item => {
        const checkbox = item.querySelector('.ingredient-checkbox');
        const priceEl = item.querySelector('.ingredient-price');
        const qtyEl = item.querySelector('.ingredient-quantity');
        if (!checkbox) return;
        const qty = parseFloat(checkbox.dataset.quantity || '0');
        const ppu = parseFloat(checkbox.dataset.ppu || '0');
        const unit = checkbox.dataset.unit || '';
        const multiplier = defaultServings > 0 ? (servings / defaultServings) : 1.0;
        const adjustedQty = qty * multiplier;
        const adjustedPrice = ppu * adjustedQty;
        if (qtyEl) qtyEl.textContent = `${adjustedQty.toFixed(2)} ${unit}`;
        if (priceEl) priceEl.textContent = `- ₹${adjustedPrice.toFixed(2)}`;
        checkbox.dataset.price = adjustedPrice.toFixed(2);
    });
}

function saveLater() {
    alert('Save for Later feature coming soon!');
    // TODO: Implement saved recipes functionality
}


