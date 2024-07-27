
$(document).ready(function () {

    function validateForm(data) {
        var errors = {};
        if (!data.name.trim()) errors.name = 'Name cannot be blank.';
        if (!data.image.trim()) {
            errors.image = 'Image URL cannot be blank.';
        } else {
            // A simple URL pattern; this can be made more complex as needed
            var pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
            if (!pattern.test(data.image)) {
                errors.image = 'Invalid URL format for image.';
            }
        }
        if (!data.description.trim()) errors.description = 'Description cannot be blank.';
        if (!data.rating.trim() || isNaN(data.rating) || data.rating < 0 || data.rating > 5) errors.rating = 'Rating must be between 0 and 5.';
        if (!data.address.trim()) errors.address = 'Address cannot be blank.';
        if (!data.example_drinks || data.example_drinks.length === 0 || data.example_drinks.some(drink => !drink.trim())) {
            errors['example-drinks'] = 'At least one example drink is required.';
        }
        if (!data.category) errors.category = 'Please select a category.';
        return errors;
    }

    $('#add-item-form input, #add-item-form textarea, #add-item-form select').on('keyup change', function () {
        var field = $(this).attr('name');
        // Convert 'example_drinks[]' to 'example_drinks'
        field = field.replace('[]', '');
        // If the field is valid or non-empty, clear its error message
        if ($(this).val().trim() !== '') {
            $('#' + field + '-error').text('');
        }
    });

    $('#image').on('keyup change', function () {
        var urlValue = $(this).val().trim();
        if (urlValue === '') {
            $('#image-error').text('Image URL cannot be blank.');
        } else {
            var pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
            if (!pattern.test(urlValue)) {
                $('#image-error').text('Invalid URL format for image.');
            } else {
                $('#image-error').text('');
            }
        }
    });

    $('#rating').on('keyup change', function () {
        var ratingValue = parseFloat($(this).val().trim());
        if (isNaN(ratingValue) || ratingValue < 0 || ratingValue > 5) {
            $('#rating-error').text('Rating must be between 0 and 5.');
        } else {
            $('#rating-error').text('');
        }
    });

    $('#example-drinks').on('keyup change', 'input', function () {
        var allFilled = true;
        var inputs = $('#example-drinks input');
        inputs.each(function () {
            if (!$(this).val().trim()) {
                allFilled = false;
                return false; // Break the loop
            }
        });

        if (inputs.length >= 2 && allFilled) {
            $('#example-drinks-error').text('');
        } else {
            $('#example-drinks-error').text('At least two example drinks are required, with no empty fields.');
        }
    });

    $('#search-form').submit(function (e) {
        e.preventDefault();
        var inputField = $(this).find('input[name="query"]');
        var query = inputField.val().trim();
        if (query) {
            // Only redirect if query is not empty
            window.location.href = '/search?query=' + encodeURIComponent(query);
        } else {
            // Reset and focus on the search box if the query is empty or just whitespace
            inputField.val('').focus();
        }
    });

    $('.drink-word').click(function () {
        var query = $(this).text();
        window.location.href = '/search?query=' + query;
    });

    $('#add-drink').click(function () {
        // Add new input for additional drinks
        $('#example-drinks').append('<div class="form-group"><input type="text" class="form-control" placeholder="Enter any example drink here..." name="example_drinks[]" required></div>');
    });

    $('#add-item-form').submit(function (e) {
        e.preventDefault();

        var formData = $(this).serializeArray(); // Convert form data to an array
        var data = {};
        formData.forEach(function (field) {
            // Handle array of example_drinks separately
            if (field.name === 'example_drinks[]') {
                if (!data.example_drinks) {
                    data.example_drinks = [];
                }
                data.example_drinks.push(field.value);
            } else {
                data[field.name] = field.value;
            }
        });

        var formErrors = validateForm(data);
        if (Object.keys(formErrors).length > 0) {
            // Display errors
            for (var error in formErrors) {
                $('#' + error + '-error').remove(); // Remove existing error messages
                $('<div/>', {
                    'id': error + '-error',
                    'class': 'error-message',
                    'text': formErrors[error]
                }).insertAfter('#' + error);
            }
        } else {
            $.ajax({
                type: 'POST',
                url: '/add',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                success: function (response) {
                    $('#success-message').text(response.message).show();
                    $('#add-item-form').trigger('reset'); // Clear the form
                    $('#name').focus(); // Set focus to the first input
                    $('#view-link').remove(); // Remove existing view link if any
                    $('<a/>', {
                        text: 'See it here',
                        href: '/view/' + response.new_item_id,
                        id: 'view-link',
                        class: 'btn btn-success submit-form mb-3'
                    }).insertAfter('#success-message');
                },
                error: function (xhr, textStatus, errorThrown) {
                    // Generic error message
                    var errorMessage = 'An error occurred while submitting the form. Please try again.';
                    alert(errorMessage);
                }
            });
        }
    });
    // Function to handle clicking "Edit Data" button in the view page
    $('#edit-data-button').click(function () {
        var itemId = $(this).data('id');
        window.location.href = '/edit/' + itemId;
    });

    // Function to handle form submission for editing an item
    $('#edit-item-form').submit(function (e) {
        e.preventDefault();
        var formData = $(this).serializeArray(); // Convert form data to an array
        var itemId = $('#discard-changes').data('item-id'); // Retrieve item ID from the discard changes button
        var data = {};
        formData.forEach(function (field) {
            // Handle array of example_drinks separately
            if (field.name === 'example_drinks[]') {
                if (!data.example_drinks) {
                    data.example_drinks = [];
                }
                data.example_drinks.push(field.value);
            } else {
                data[field.name] = field.value;
            }
            data.id = itemId;
        });

        var formErrors = validateForm(data);
        if (Object.keys(formErrors).length > 0) {
            // Display errors
            for (var error in formErrors) {
                $('#' + error + '-error').remove(); // Remove existing error messages
                $('<div/>', {
                    'id': error + '-error',
                    'class': 'error-message',
                    'text': formErrors[error]
                }).insertAfter('#' + error);
            }
        } else {
            $.ajax({
                type: 'POST',
                url: '/edit/' + itemId, // Assuming your edit route is '/edit/<id>'
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                success: function (response) {
                    // Redirect to the view page after successful edit
                    window.location.href = '/view/' + itemId;
                },
                error: function (response) {
                    errorText = 'An error occurred while submitting the form.';
                    alert(errorText);
                }
            });
        }
    });

    // Function to handle clicking "discard changes" button
    $('#discard-changes').click(function () {
        if (confirm("Are you sure you want to discard changes?")) {
            var itemId = $(this).data('item-id');
            window.location.href = '/view/' + itemId;
        }
    });
});