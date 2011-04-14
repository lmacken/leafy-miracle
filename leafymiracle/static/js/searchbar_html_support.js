// Add the hook in for catcomplete.
// We add it here instead of a tw2.jquery_ui template because it must
// be executed before *any* other plugins reference jquery ui proper

$(document).ready(function() {
        $.widget( "custom.catcomplete", $.ui.autocomplete, {
                _renderItem: function( ul, item) {
                        return $( "<li></li>" )
                        .data( "item.autocomplete", item )
                        .append( $( "<a></a>" ).html( item.label ) )
                        .appendTo( ul );
                }
        });
});
