// Add the hook in for catcomplete.
// We add it here instead of a tw2.jquery_ui template because it must
// be executed before *any* other plugins reference jquery ui proper

$(document).ready(function() {
        $.widget( "custom.catcomplete", $.ui.autocomplete, {
                _renderMenu: function( ul, items ) {
                        var self = this, currentCategory = "";
                        $.each( items, function( index, item ) {
                                if ( item.category != currentCategory ) {
                                        ul.append( '<li class="ui-autocomplete-category">' + item.category + "</li>" );
                                        currentCategory = item.category;
                                }
                                self._renderItem( ul, item );
                        });
                },
                _renderItem: function( ul, item) {
                        return $( "<li></li>" )
                        .data( "item.autocomplete", item )
                        .append( $( "<a></a>" ).html( item.label ) )
                        .appendTo( ul );
                }
        });
});
