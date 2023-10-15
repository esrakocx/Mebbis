
$(document).ready(function() {
    $('#duzenlenmisveriler2').DataTable();

    $('#duzenlenmisveriler2').on('click', '.update-button', function() {
        var row = $(this).closest('tr');
        var rowData = row.find('td').map(function() {
            return $(this).text();
        }).get();

        alert('Update data: ' + rowData.join(', '));
    });
});
