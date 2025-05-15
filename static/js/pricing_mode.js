(function($) {
    $(document).ready(function() {
        function toggleDayFields() {
            var mode = $('#id_mode').val();
            var dayFields = ['#id_lundi', '#id_mardi', '#id_mercredi', '#id_jeudi', '#id_vendredi', '#id_samedi'];
            if (mode === 'daily') {
                dayFields.forEach(function(field) {
                    $(field).parent().parent().show();
                });
            } else { // 'product'
                dayFields.forEach(function(field) {
                    $(field).parent().parent().hide();
                });
            }
        }

        // Initial call
        toggleDayFields();

        // Bind change event
        $('#id_mode').change(toggleDayFields);
    });
})(django.jQuery);