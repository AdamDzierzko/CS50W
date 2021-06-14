document.addEventListener('DOMContentLoaded', function() {

if (document.querySelector('#compose-form-movie')) {
    document.querySelector('#compose-form-movie').onsubmit = () => { addmovie() };
};
if (document.querySelector('#edit-form-movie')) {
    document.querySelector('#edit-form-movie').onsubmit = () => { editmovie() };
};
if (document.querySelector('#compose-form-genere')) {
    document.querySelector('#compose-form-genere').onsubmit = () => { addgenere() };
    document.querySelector('#compose-form-actor').onsubmit = () => { addactor() };
};
if (document.querySelector('#compose-form-grade')) {
    document.querySelector('#compose-form-grade').onsubmit = () => { addgrade() };
};
if (document.querySelector('#edit-form-grade')) {
    document.querySelector('#edit-form-grade').onsubmit = () => { editgrade() };
};

if (document.querySelector('#compose-form-coment')) {
    document.querySelector('#compose-form-coment').onsubmit = () => { addcoment() };
};
if (document.querySelector('#compose-form-edit')) {
    document.querySelector('#compose-form-edit').onsubmit = () => { editcoment() };
};
});

function addmovie() {

    let actors = [];
    let actors_checkbox = document.querySelectorAll('#actor:checked');

    for (let i = 0; i < actors_checkbox.length; i++) {
        actors.push(actors_checkbox[i].value)
    };

    let title = document.querySelector('#title').value;
    let genere = document.querySelector('#genere').value;
    let director = document.querySelector('#director').value;
    let description = document.querySelector('#description').value;
    let year = document.querySelector('#year').value;

    fetch('/addmovie', {
        method: 'POST',
        body: JSON.stringify({
            actors : actors,
            genere: genere,
            title: title,
            director: director,
            description: description,
            year: year

        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href="/";
    } else {
        alert(result.error);
    }
    });
}

function editmovie() {

    let actors = [];
    let actors_checkbox = document.querySelectorAll('#actor:checked');

    for (let i = 0; i < actors_checkbox.length; i++) {
        actors.push(actors_checkbox[i].value)
    };

    let title = document.querySelector('#title').value;
    let genere = document.querySelector('#genere').value;
    let director = document.querySelector('#director').value;
    let description = document.querySelector('#description').value;
    let year = document.querySelector('#year').value;
    let movie_id = document.querySelector('#edit_movie').value;

    console.log(movie_id);

    fetch(`/edit_movie/${movie_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            actors : actors,
            genere: genere,
            title: title,
            director: director,
            description: description,
            year: year
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href="/";
    } else {
        alert(result.error);
    }
    });
}

function addgenere() {

    let genere_name = document.querySelector('#genere-text').value;

    fetch('/addgenere', {
        method: 'POST',
        body: JSON.stringify({
            genere_name: genere_name,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href="/config";
    } else {
        alert(result.error);
    }
    });
}

function addactor() {

    let actor_name = document.querySelector('#actor-text').value;

    fetch('/addactor', {
        method: 'POST',
        body: JSON.stringify({
            actor_name: actor_name,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href="/config";
    } else {
        alert(result.error);
    }
    });
}

function addgrade() {

    let grade = document.querySelector('#grade').value;
    let movie_id = document.querySelector('#grade_movie').value;

        fetch('/addgrade', {
        method: 'POST',
        body: JSON.stringify({
            grade: grade,
            movie_id: movie_id,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href="/";
    } else {
        alert(result.error);
    }
    });
}

function editgrade() {

    let grade = document.querySelector('#grade_edit').value;
    let grade_id = document.querySelector('#edit_grade_id').value;
    let grade_type = document.querySelector('#edit_grade_type').value;
    let movie_id = document.querySelector('#grade_movie').value;

        fetch(`/edit_grade/${grade_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            grade: grade,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        if (grade_type == "coment") {
            document.location.href=`/coment_index/${movie_id}`;
        } else {
            document.location.href="/";
        }
    } else {
        alert(result.error);
    }
    });
}

function addcoment() {

    let coment_text = document.querySelector('#coment_text').value;
    let movie_id = document.querySelector('#coment_movie').value;

        fetch('/addcoment', {
        method: 'POST',
        body: JSON.stringify({
            coment_text: coment_text,
            movie_id: movie_id,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href=`/coment_index/${movie_id}`;
    } else {
        alert(result.error);
    }
    });
}

function editcoment() {

    let coment_text = document.querySelector('#coment_edit').value;
    let movie_id = document.querySelector('#coment_edit_movie').value;
    let coment_id = document.querySelector('#coment_edit_id').value;

        fetch(`/edit_coment/${coment_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            coment_text: coment_text,
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "OK") {
        document.location.href=`/coment_index/${movie_id}`;
    } else {
        alert(result.error);
    }
    });
}

function menu() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}