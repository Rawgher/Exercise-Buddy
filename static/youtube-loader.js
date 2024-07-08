document.addEventListener('DOMContentLoaded', function() {
 // Show loader and hide videos initially
 $('#loader').show();
 $('#videos').hide();

 // Once the window has fully loaded, hide the loader and show the videos
 $(window).on('load', function() {
     $('#loader').hide();
     $('#videos').show();
 });
});