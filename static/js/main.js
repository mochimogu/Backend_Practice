

function viewBlog(e) {

    console.log(e)

    window.localStorage.setItem('index', e);

    window.location.href = `/edit/${e}`

}


