import { createRef, useEffect, useRef, useState } from 'react';
import Section from './Section';
import QuestionAnswer from './QuestionAnswer';

export default function FAQ(){

    return (
        <Section section-name={"faq"}>
            <h1 className="faq-header">Frequently asked questions</h1>
            <div className="grid-container">
                <div className="grid-col">
                    <QuestionAnswer
                        question="What is Electrodermal Activity (EDA)?" 
                        answers={[
                            "EDA, often referred to as skin conductance, measures changes in the electrical conductivity of the skin. It's a physiological response linked to emotional arousal and stress."
                        ]}
                    />
                    <QuestionAnswer 
                        question="What are EDA artifacts?" 
                        answers={[
                            "EDA signals can be contaminated by various artifacts, such as movement artifacts, sensor noise, and temperature fluctuations.",
                            "These artifacts can significantly impact the accuracy of stress detection and other analyses."
                        ]}
                    />
                    <QuestionAnswer 
                        question="How does your tool address EDA artifact recognition and correction?" 
                        answers={[
                            "Our tool employs a hybridized LSTM-SVM model to effectively detect and correct EDA artifacts.",
                            "The LSTM component captures complex temporal dependencies in the EDA signal, while the SVM provides a robust classification mechanism."
                        ]}
                    />
                    <QuestionAnswer 
                        question="Why combine LSTM and SVM?" 
                        answers={[
                            "LSTM: Captures long-term dependencies in the time series data, making it suitable for complex patterns in EDA signals.",
                            "SVM: Provides a strong classification performance, especially in high-dimensional spaces, and is less prone to overfitting."
                        ]}
                    />
                    <QuestionAnswer 
                        question="What are the limitations of your tool?" 
                        answers={[
                            "Like any machine learning model, our tool's performance depends on the quality of the input data. Noisy data or artifacts that are significantly different from the training data may impact the accuracy of the model. Additionally, the tool's performance might be influenced by individual physiological differences."
                        ]}
                    />
                </div>
                <div className="grid-col">
                    <QuestionAnswer 
                        question="How does your tool handle imbalanced datasets, which are common in EDA research?" 
                        answers={[
                            "Although this is still a pertinent problem in EDA research we chose to delimit the scope of this research to using only the hybridized approach",
                            "Recommendations for the conducted research does include handling class imbalance such using the ff:",
                            "Class weighting: Assigning higher weights to the minority class during training.",
                            "Oversampling: Increasing the number of samples in the minority class through techniques like SMOTE.",
                            "Undersampling: Reducing the number of samples in the majority class."
                        ]}
                    />
                    <QuestionAnswer 
                        question="How does your tool handle different sampling rates?" 
                        answers={[
                            "For now the tool is designed to handle only a 128hz sampling rate as this was the frequency the machine learning methods trained on as well as the researchers proposed LSTM-SVM. The windowing technique used was to extract features."
                        ]}
                    />
                    <QuestionAnswer 
                        question="Can your tool be used for real-time applications?" 
                        answers={[
                            "While our current implementation is focused on offline analysis, the underlying techniques can be adapted for real-time applications. However, real-time implementation would require careful consideration of computational efficiency and latency constraints."
                        ]}
                    />
                    <QuestionAnswer 
                        question="How can researchers use your tool?" 
                        answers={[
                            "Researchers can use our tool to:",
                            "Preprocess EDA data to remove artifacts.",
                            "Extract relevant features from the cleaned data.",
                            "Train and evaluate machine learning models for stress detection and other applications.",
                            "Gain insights into the underlying physiological mechanisms of stress and emotion using the resulting corrected signals."
                        ]}
                    />
                </div>
            </div>
        </Section>
    )
}
