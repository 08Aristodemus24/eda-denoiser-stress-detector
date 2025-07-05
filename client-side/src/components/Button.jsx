import { useContext } from "react";
import { ThemeContext } from "../contexts/ThemeContext";
import { DesignsContext } from "../contexts/DesignsContext";
import { FormInputsContext } from "../contexts/FormInputsContext";

export default function Button({ children }){
    // initialize and define theme of component by using
    // context
    let style;
    const designs = useContext(DesignsContext);
    const themes = useContext(ThemeContext);

    /** where to actually display or undisplay path object when either show raw or show correct states are changed */
    let { initSprSheet, useDemo } = useContext(FormInputsContext);

    const { design, theme } = themes;
    
    // sometimes themes context will contain only the design 
    // and not the theme key so check if theme key is in themes
    if('theme' in themes){
        style = designs[design][theme];
    }else{
        style = designs[design];
    }

    // based on the context provider of wrapped Form containing
    // all its states we use the state appropriate to the Button
    // component and its setter to set from this component the state of
    // the form
    let { handleSubmit } = useContext(FormInputsContext);

    const toggle = design.includes('neomorphic') ? (event) => {
        console.log(event.target.classList);
        if(event.target.classList.contains('clicked')){
            event.target.classList.remove('clicked');
        }else{
            event.target.classList.add('clicked');
        }
    } : null;

    console.log(`iniSprSheet is empty? ${initSprSheet.length === 0 ? true : false}`);
    console.log(`use demo? ${useDemo}`)

    // unlock button only if use Demo is true or initSprSheet
    // is not null or both

    // if initSprSheet is empty set to (true) and if useDemo (false) set enable to false
    // if initSprSheet has set to (false) and if useDemo (false) set enable to true
    // if initSprSheet is empty set to (true) and if useDemo (true) set enable to true
    // if initSprSheet has set to (false) and if useDemo (true) set enable to true

    const xand = (a, b) => !(a ^ b);
    const spreadsheetEmpty = initSprSheet.length === 0 ? true : false;
    const enableButton = !xand(spreadsheetEmpty, useDemo)

    return (
        <div className={`submit-btn-container ${design}`} style={style}>
            <button
                disabled={enableButton}
                type="submit"
                className={`submit-btn ${design}`} 
                onMouseDown={toggle} 
                onMouseUp={toggle} 
                onClick={handleSubmit}
            >
                Submit
            </button>
        </div>
    );
}