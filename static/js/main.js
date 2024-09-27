

function viewBlog(e) {

    console.log(e)

    window.localStorage.setItem('index', e);

    window.location.href = `/edit/${e}`

}

function readBlog(t) {

    console.log(t);

    window.localStorage.setItem('title', t);

    window.location.href = `/read/${t}`

}

const filter = document.getElementById('filterButton');

if(filter !== null) {

    filter.addEventListener('click', async () => {

        const cat = document.getElementById('cat').value;

        console.log(cat);
        window.location.href = `/browse/category/${cat}`        
        // if(cat !== "") {

        // }

    })


}


