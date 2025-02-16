$(document).ready(function() {
    let selectedProducts = [];

    function updateDropdown(url, target, parameterName, parameterValue) {
        if (parameterValue === '0') {
            $(target).html('<option value="0">Выберите товар</option>');
            return;
        }

        $.get(url, { [parameterName]: parameterValue }, function(data, status) {
            const currentProduct = $(target).val();
            $(target).html(data);    
            $(target).val(currentProduct);
            filterProducts();
        });
    }

    function filterProducts() {
        $('.product-select').each(function() {
            const currentSelect = $(this);
            const currentVal = currentSelect.val();

            currentSelect.find('option').each(function() {
                if (selectedProducts.includes($(this).val()) && $(this).val() != currentVal) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
        });
    }

    $('#form-container').on('change', '.warehouse-select', function() {
        const formRow = $(this).closest('.form-row');
        const quantityInput = formRow.find('.quantity-input');
        const priceInput = formRow.find('.price-input');
        const totalInput = formRow.find('.total-input');

        quantityInput.val('');
        priceInput.val('');
        totalInput.val('');

        const productSelect = formRow.find('.product-select');
        updateDropdown("/get-product/", productSelect, "warehouse_id", $(this).val());
    });

    $('#form-container').on('change', '.product-select', function() {
        const formRow = $(this).closest('.form-row');
        const quantityInput = formRow.find('.quantity-input');
        const priceInput = formRow.find('.price-input');
        const totalInput = formRow.find('.total-input');
        const selectedOption = $(this).find(':selected');
        
        const quantity = selectedOption.data('quantity');
        const price = selectedOption.data('price');

        quantityInput.attr('min', 1);
        quantityInput.attr('max', quantity);
        quantityInput.attr('placeholder', 'От 1 До ' + quantity);

        priceInput.val(price);
        totalInput.val(0);
        recalculateTotal(formRow);

        selectedProducts = $('.product-select').map(function() {
            return $(this).val();
        }).get();

        filterProducts();
    });

    $('#form-container').on('input', '.quantity-input', function() {
        const formRow = $(this).closest('.form-row');
        recalculateTotal(formRow);
    });

    function recalculateTotal(formRow) {
        const price = parseFloat(formRow.find('.price-input').val());
        let quantity = parseFloat(formRow.find('.quantity-input').val());
        const maxQuantity = parseFloat(formRow.find('.quantity-input').attr('max'));
        const totalInput = formRow.find('.total-input');

        if (isNaN(quantity)) {
            quantity = null;
        } else if (quantity > maxQuantity) {
            quantity = maxQuantity;
        } else if (quantity < 1) {
            quantity = 1;
        }

        if (quantity === null) {
            totalInput.val('');
        } else {
            formRow.find('.quantity-input').val(quantity);
            const total = quantity * price;
            totalInput.val(total.toFixed(2));
        }
    }

    $('#add-form').click(function() {
        const newFormRow = $('.form-row:first').clone();
        newFormRow.find('select').val('0');
        newFormRow.find('input').val('');
        newFormRow.find('.product-select').html('<option value="0">Выберите товар</option>');
        newFormRow.find('.quantity-input').attr('max', '');
        
        // Append new row inside the table body
        $('#form-container table tbody').append(newFormRow);

        filterProducts();
    });

    $('#remove-form').click(function() {
        if ($('.form-row').length > 1) {
            $('.form-row:last').remove();
            selectedProducts = $('.product-select').map(function() {
                return $(this).val();
            }).get();
            filterProducts();
        }
    });

    $('#sell-form').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting normally

        const formData = $(this).serialize();  // Serialize form data

        $.ajax({
            url: "{% url 'sell' %}",  // URL to handle the form submission
            type: 'POST',
            data: formData,
            success: function(response) {
                // Handle successful form submission
                window.location.href = "/sell";  // Redirect or update the page
            },
            error: function(xhr, status, error) {
                // Handle form validation errors
                const errors = xhr.responseJSON.errors;  // Assuming errors are returned as JSON
                let errorMessages = '';

                for (const field in errors) {
                    errorMessages += `<p>${errors[field]}</p>`;
                }

                $('#error-messages').html(errorMessages);  // Display errors
            }
        });
    });
});

function isNumberKey(evt) {
  var charCode = (evt.which) ? evt.which : evt.keyCode
  if (charCode > 31 && (charCode < 48 || charCode > 57))
    return false;
  return true;
}