const container = document.getElementById('editor');
const toolbar = [
    [{'header': ['2',false]}],
    [{'font': []}],
    [{'size' : ['small', false, 'large', 'huge'] }],
    [{'color': []}, {'background' : []}],
    ['bold', 'italic', 'underline', 'strike'],
    [{'align': ['', 'center', 'right', 'justify']}],
    [{'list': 'ordered'}, {'list': 'bullet'}],
    [{ 'script': 'sub'}, { 'script': 'super' }],
    ['clean'],

];

const quill = new Quill(container, {
    modules : {
        toolbar : toolbar
    },
    theme : 'snow',
    placeholder : 'start blogging...'
});

const saveButton = document.getElementById('saveButton');

if(saveButton !== null) {
    saveButton.addEventListener('click', async () => {
        console.log("clicked!")
        //potential when publishing
        // const delta = quill.getSemanticHTML();
        const title = document.getElementById('title').value;
        const category = document.getElementById('cat').value;
        const delta = quill.getContents();
    
        console.log(delta);
        console.log(title, category);
    
        const tags = [
            {'tech' : ['tech', 'programming', 'pc']},
            {'food' : ['recipe', 'spice', 'food']},
            {'fitness' : ['gym', 'exercise', 'diet']},
            {'politics' : ['republican', 'democrat', 'congress']},
            {'philosophy' : ['peace', 'mindfulness', 'thinker']},
            {'science' : ['newton', 'biology', 'physics']}
        ];
    
        const tag = tags.find(element => element.hasOwnProperty(category));
        console.log(tag);
    
        sending = {
            'title' : title,
            'category' : category,
            'delta' : delta,
            'tags' : tag[category]
        }
    
        const response = await fetch('/saveBlog', {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify(sending)
        });
    
        const results = await response.json();
    
        console.log(results);
    
    })
}

console.log(window.location.pathname)

async function loadData(e) {
    const response = await fetch(`/api/edit/${e}`);
    
    if(response.ok) {
        const results = await response.json();
        console.log(results);

        document.getElementById('title').value = results.title;
        document.getElementById('cat').value = results.category;

        quill.setContents(results.delta);

        const updateButton = document.getElementById('updateButton')

        if(updateButton !== null) {

            updateButton.addEventListener('click', async () => {

                const title = document.getElementById('title').value;
                const category = document.getElementById('cat').value;
                const delta = quill.getContents();
            
                console.log(delta);
                console.log(title, category);
            
                const tags = [
                    {'tech' : ['tech', 'programming', 'pc']},
                    {'food' : ['recipe', 'spice', 'food']},
                    {'fitness' : ['gym', 'exercise', 'diet']},
                    {'politics' : ['republican', 'democrat', 'congress']},
                    {'philosophy' : ['peace', 'mindfulness', 'thinker']},
                    {'science' : ['newton', 'biology', 'physics']}
                ];
            
                const tag = tags.find(element => element.hasOwnProperty(category));
                console.log(tag);
            
                sending = {
                    'id' : e,
                    'title' : title,
                    'category' : category,
                    'delta' : delta,
                    'tags' : tag[category]
                }
            
                const response = await fetch(`/api/update/${e}`, {
                    method : 'POST',
                    headers : {
                        'Content-Type' : 'application/json'
                    },
                    body : JSON.stringify(sending)
                });
            
                const results = await response.json();
                
                console.log(results);
            })
        }

    } else {
        console.log(response.status);
    }
}


if(window.localStorage.getItem('index') !== null && window.location.href.match('/edit/')) {

    const e = window.localStorage.getItem('index');
    loadData(e);
}

const publishButton = document.getElementById('publishButton');


if(publishButton !== null) {
    const e = window.localStorage.getItem('index');

    publishButton.addEventListener('click', async () => {

        console.log("pressed")

        const published = quill.getSemanticHTML();


        sending = {
            'id' : e,
            'delta' : published
        }

        const response = await fetch(`/api/published/${e}`, {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify(sending)
        })

        const results = await response.json();
        
    })
}

