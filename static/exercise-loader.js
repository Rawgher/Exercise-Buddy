document.addEventListener('DOMContentLoaded', function() {
    // Show loader and hide content initially
    $('#loader').show();
    $('#content').hide();
   
    // Once the window has fully loaded, hide the loader and show the content
    $(window).on('load', function() {
        $('#loader').hide();
        $('#content').show();
    });
   });