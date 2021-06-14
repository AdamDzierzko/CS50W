document.addEventListener('DOMContentLoaded', function() {
like();
follow();
document.querySelector('#compose-form').onsubmit = () => { add() };
document.querySelector('#compose-edit').onsubmit = () => { edit() };
});

function add() {

let text = document.querySelector('#post-text').value;

    fetch('/add', {
        method: 'POST',
        body: JSON.stringify({
            text: text
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "Email sent successfully.") {
    } else {
        alert(result.error);
    }
    });
}

function edit() {

let text = document.querySelector('#post-edit').value;
let id = document.querySelector("#id-edit").getAttribute('value');

    fetch(`/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: text,
            postid: id
        }),
    })
    .then(response => response.json())
    .then(result => {
     if (result.message == "Email sent successfully.") {
        document.location.href="/";
     } else {
        alert(result.error);
     }
     });
}

function like() {

like = document.querySelectorAll('#like');
like.forEach( (post) => {
    post.addEventListener('click', () => {
        let id = post.getAttribute('data-value');
        let w = post.getAttribute('data-type');
        let u = post.getAttribute('data-user');

        fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            }),
        })
        .then(response => response.json())
        .then(result => {
        if (result.message == "Email sent successfully.") {
            if ( w == 1) {
            document.location.href="/";
            } else {
            document.location.href=`/profil/${u}`;
            }
        } else {
            alert(result.error);
        }
        });
     });
    });

dislike = document.querySelectorAll('#dislike');
dislike.forEach( (post) => {
    post.addEventListener('click', () => {
        let id = post.getAttribute('data-value');
        let w = post.getAttribute('data-type');
        let u = post.getAttribute('data-user');

        fetch(`/dislike/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            }),
        })
        .then(response => response.json())
        .then(result => {
        if (result.message == "Email sent successfully.") {
            if ( w == 1) {
            document.location.href="/";
            } else {
            document.location.href=`/profil/${u}`;
            }
        } else {
            alert(result.error);
        }
        });
     });
    });

}

function follow() {

follow = document.querySelectorAll('#follow');
follow.forEach( (f) => {
    f.addEventListener('click', () => {

        let id = f.getAttribute('data-value');

        fetch(`/follow/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            }),
        })
        .then(response => response.json())
        .then(result => {
        if (result.message == "Email sent successfully.") {
            location.reload();
        } else {
            alert(result.error);
        }
        });
     });
    });

unfollow = document.querySelectorAll('#unfollow');
unfollow.forEach( (f) => {
    f.addEventListener('click', () => {

        let id = f.getAttribute('data-value');

        fetch(`/unfollow/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            }),
        })
        .then(response => response.json())
        .then(result => {
        if (result.message == "Email sent successfully.") {
            location.reload();
        } else {
            alert(result.error);
        }
        });
     });
    });

}
