/**
 * Returns date object
 *
 * @param int value  Time in seconds counted from midnight
 * @returns Date Date object based on input value
 */
function parseInterval(value) {
    var result = new Date(1, 1, 1);
    result.setMilliseconds(value * 1000);
    return result;
}


jQuery(function($) {
    loading = $('#loading');

    /**
     * Get users list after the page DOM is loaded
     */
    $.getJSON('/api/v1/users', function(result) {
        var $dropdown = $('#user_id');

        // Populate users dropdown with data
        $.each(result, function(item) {
            $dropdown.append(
                $('<option />').data('image_url', this.image_url)
                               .val(this.user_id)
                               .text(this.name)
            );
        });

        // Display user image when dropdown value changes
        $dropdown.change(function(e) {
            var $option = $('option:selected', this);
            $('#user_info').html(
                $('<img/>').attr('src', $option.data('image_url'))
                           .attr('alt', $option.text())
                           .attr('title', $option.text())
            );
        });

        $dropdown.show();
        loading.hide();
    });
});
