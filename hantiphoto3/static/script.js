function updateStatus(reservation_id, status) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/update_status/${reservation_id}`);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log("Status updated");
        }
    };
    xhr.send(`status=${status ? 1 : 0}`);
}

function copyNumber(number) {
    navigator.clipboard.writeText(number);
    alert("전화번호가 복사되었습니다: " + number);
}
