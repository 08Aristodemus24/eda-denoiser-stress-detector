import { useEffect, useState } from 'react';

export default function QuestionAnswer({ question, answers }){
    let [isOpen, setIsOpen] = useState(false);

    // define styles for answer paragraph if isOpen state
    // is true or false
    const answerStyle = {
        // height: isOpen === true ? "auto" : 0
    }

    const toggleAnswer = (event) => {
        console.log("clicked");
        setIsOpen(!isOpen);
    }

    const answersContainers = answers.map((answer, index) => {
        return <p key={index} className="content" style={answerStyle}>
            {answer}
        </p>
    })

    // if offsets is initially undefined set style to null initially
    // style={!offsets ? null : {'width': offsets.offset_width}}
    return (
        <div className={`qa-container ${isOpen === true ? "opened" : null}`}>
            <h3 className="question">
                <p className="content">{question}</p>
                <div className="toggler" onClick={toggleAnswer}></div>
            </h3>
            <div className="answer">
                <div>{answersContainers}</div>
            </div>
        </div>
    );
}