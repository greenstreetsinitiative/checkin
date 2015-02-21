var showInvoiceTextbox = function() {
    $('#invoice').change(function() {
        if($('#invoice:checked').length === 1) {
            $("#invoice_container").removeClass('hidden');
        } else {
            $("#invoice_container").addClass('hidden');
        }
    });
};

$(document).ready(function() {
    showInvoiceTextbox();
});
