import { useContext, useEffect } from "react";
import { ThemeContext } from "../contexts/ThemeContext";
import { DesignsContext } from "../contexts/DesignsContext";
import { FormInputsContext } from "../contexts/FormInputsContext";
import { S3 } from "aws-sdk";

export default function Radio(props){
    // initialize and define theme of component by using
    // context
    let style;
    const designs = useContext(DesignsContext);
    const themes = useContext(ThemeContext);
    const { design, theme } = themes;
    
    // sometimes themes context will contain only the design 
    // and not the theme key so check if theme key is in themes
    if('theme' in themes){
        style = designs[design][theme];
    }else{
        style = designs[design];
    }

    // console.log(props);

    // based on the context provider of wrapped Form containing
    // all its states we use the state appropriate to the ImageInput
    // component and its setter to set from this component the state of
    // the form
    const { useDemo, setUseDemo, initSprSheet } = useContext(FormInputsContext);

    const handleCheck = async (event) => {
        // set boolean of check input to the
        // opposite of it
        setUseDemo((curr_state) => !curr_state);
        // const s3 = new S3();
        // const params = {
        //     Bucket: "eda-denoiser-stress-detector-bucket",
        //     Key: "/oxused_expert2.csv",
        // };

        // const fileStream = s3.getObject(params).createReadStream();
        // console.log(fileStream)
    }


    useEffect(() => {
        console.log(useDemo)
    }, [useDemo]);

    return (
        <div className={`radio-container ${design}`} style={style}>
                
            <input 
                type="radio"
                id="radio"
                disabled={initSprSheet.length === 0 ? false : true}
                // if for example user wants checkbox to show artifacts
                // then name of input must be show_artifacts, so when 
                // processed by server dictioonary can be easily accessed 
                // through show_artifacts key
                name={`${props["name"]}`}
                className={`radio-field ${design}`} 
                checked={useDemo}
                value={useDemo}
                onChange={handleCheck}
            ></input><label htmlFor="radio" className="radio-label">{props["label"]}</label>
        </div>
    );
}