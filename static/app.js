document.addEventListener('DOMContentLoaded', function() {
    var picker = new Pikaday({
        field: document.getElementById('datepicker'),
        format: 'YYYY-MM-DD',
        onSelect: function(date) {
            $('#workoutDate').val(picker.toString());
            $('#workoutModal').modal('show');
        }
    });

    // Open datepicker when clicking on the calendar icon
    $('.input-group-append').on('click', function() {
        picker.show();
    });

    $('#workoutForm').on('submit', function(event) {
        event.preventDefault();

        var form = $(this);
        $.post(form.attr('action'), form.serialize(), function(data) {
            $('#workoutModal').modal('hide');
            picker.setDate(null);  // Clear the date after submitting
            location.reload();  // Reload the page to show the updated workout entries and streak
        });
    });
});