$(document).ready(function() {
    $('#form-request-tab').click(function () {
        document.getElementById('form-request').style.display = 'block';
        document.getElementById('submit-request').style.display = 'none';
    });

    $('#submit-request-tab').click(function () {
        document.getElementById('submit-request').style.display = 'block';
        document.getElementById('form-request').style.display = 'none';
    });

    $('#form-request-button').click(function () {
        var begin = $('#begin-input').val();
        var end = $('#end-input').val();
        var participantType = $('#participant-type-input').val();
        var participantId = $('#participant-id-input').val();
        $.post('/', {'begin': begin, 'end': end, 'participant_type': participantType, 'participant_id': participantId}, function(data) {
            if (data === 'error') {
                // TODO: this thing
                alert('Incorrect something');
            }
        });
    });

    $('#submit-request-button').click(function () {
        var requestId = $('#request-id-input').val();
        $.post('/', {'request_id': requestId}, function(data) {
            if (data === 'error') {
                // TODO: this thing
                alert('Incorrect something');
            }
        });
    });
});