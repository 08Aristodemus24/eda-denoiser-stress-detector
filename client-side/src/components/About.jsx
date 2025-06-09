import Section from './Section';  

export default function Correspondence(){

    return (
        <Section section-name={"about"}>
            <h1 className="research-title">
                Application of a Hybridized LSTM-SVM
                in the Detection of Artifacts
                in Electrodermal Activity Signals
                for Stress Detection
            </h1>
            <div className="research-description">
                <p className="block-1">
                    This study exclusively aimed to address the challenges present 
                    in studies revolving around artifact recognition/detection by
                    proposing a hybridized LSTM-SVM model, where the LSTM aims to 
                    improve the shortcomings of traditional ML methods 
                    of feature extraction from time series data, specifically 
                    those involving EDA signals, by integrating higher order
                    features in addition to lower order hand crafted features 
                    used by the aforementioned studies, and wherein the integrated
                    mechanism of traditional ML-based methods to the LSTM namely the
                    Support Vector Machine (SVM) aims to equalize if not improve 
                    further the difficult to interpret architectures of CNNs by 
                    using instead much more simpler methods namely ML based ones 
                    like the SVM.
                </p>
                <p className="block-2">
                    This system moreover not only classifies artifacts
                    present in electrodermal activity data but also corrects and cleans
                    the segments of the signals that do have artifacts which can 
                    subsequently be used for arousal classification tasks in the signals i.e. stress
                    detection. The following are the benchmark papers we as undergraduate researchers chose
                    to base our study on: <a href="https://www.sciencedirect.com/science/article/abs/pii/S1746809422000052">
                    Automatic motion artifact detection in electrodermal activity data using
                    machine learning</a> by Hossain et al. (2022) or <a href="https://biosignal.uconn.edu/wp-content/uploads/sites/2503/2022/01/01_Hossain_2022_BSPC.pdf">
                    this link</a> alternatively. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC5413200/">Automatic Identification of Artifacts in Electrodermal Activity Data</a> by 
                    Taylor et al. (2015). <a href="https://www.sciencedirect.com/science/article/pii/S0957417423010837?via%3Dihub">Automatic artifact recognition and correction for electrodermal activity based on LSTM-CNN models</a> by Llanes-Jurado et al. (2023).
                    Visit the publication of our study <a href="http://dx.doi.org/10.13140/RG.2.2.34355.95525">here</a>. Note that <b>the dataset that is required in order to use test this application is also 
                    available <a href="https://data.mendeley.com/datasets/w8fxrg4pv5/2">here</a></b>
                </p>
            </div>
        </Section>
    )
}