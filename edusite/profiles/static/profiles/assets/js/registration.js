console.log('registration js')

window.addEventListener("load", (event) => {
    console.log('loaded')

    let paragraphs = document.querySelectorAll('form.form_as_p > p')


    paragraphs.forEach(paragraph => {

        paragraph.classList.add('single-form')
        let text = ''
        for (const child of paragraph.children) {
            if (child.tagName == 'LABEL') {
                text = child.innerHTML
                child.hidden = true
            }
            if (child.tagName == 'INPUT') {
                child.placeholder = text


            }
        }
    });


    document.querySelector('form.form_as_p > input[type=submit]').classList.add('btn', 'btn-primary', 'btn-hover-dark', 'w-100')
});