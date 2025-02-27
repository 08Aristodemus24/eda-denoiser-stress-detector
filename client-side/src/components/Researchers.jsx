import Section from './Section';  

export default function Researchers (){
    
    const getSvgs = ({ platform, link}) => {
        const platforms = {
            linkedin: <svg class="linkedin-icon" version="1.0" xmlns="http://www.w3.org/2000/svg" width="1344" height="1344" viewBox="0 0 1008 1008"><path d="M90.3 43.5c-41.4 7.5-75.9 38.9-87.8 80-2.3 8.2-2.5 10.1-2.5 31s.2 22.8 2.5 31.1c11.6 40.3 44.8 71 86 79.5 11.6 2.4 39.6 3.4 52.5 1.8 48.9-5.8 87.5-41.7 98.2-91.4 1.6-7.8 1.6-34.2 0-42-10-46.5-43.3-80.1-88.7-89.6-7.3-1.5-13.1-1.9-31-1.8-13.4.1-24.8.6-29.2 1.4zM725.8 342c-55.2 7-105.6 33.9-140 75-4.4 5.2-11.1 14.2-14.9 19.9l-6.9 10.4-.2-45.4-.3-45.4-108.2-.3-108.1-.2.4 139.7c.3 76.9.1 223.6-.3 326.1l-.8 186.2h217.6l-.1-193.3c-.1-168.1.1-194.3 1.4-201.6 6.8-37.4 25.7-65.5 56.6-84.1 32.4-19.5 76.3-22.1 108.5-6.5 29.6 14.3 48.3 42.3 56.5 84.5 4.5 22.8 4.3 17.2 4.7 214.2l.4 186.8h216l-.4-207.8c-.3-226 0-212.9-5.8-246.2-21-120.6-92.8-195.1-202.9-210.5-13.1-1.9-62.4-2.9-73.2-1.5zM10 682v326h217l-.2-325.8-.3-325.7-108.2-.3L10 356v326z"/></svg>,
            facebook: <svg class="facebook-icon" version="1.0" xmlns="http://www.w3.org/2000/svg" width="1344" height="1344" viewBox="0 0 1008 1008"><path d="M597.5.7c-107.1 9.3-184.2 75.9-207 178.8-6.4 28.5-6.7 34.4-7.2 111.7l-.5 70.8H231v207h152v439h213l.2-219.2.3-219.3 87.3-.3 87.2-.2-.2-103.3-.3-103.2-87.3-.3-87.3-.2.4-59.3c.3-51.7.6-60.1 2.1-66.7 5.8-25 20.1-36.2 50.6-40 4.9-.6 32.9-1 67.6-1h59.1l.6-10.7c.4-5.8.7-49.7.7-97.5V0l-87.7.2c-48.3.1-89.6.3-91.8.5z"/></svg>,
            github: <svg class="github-icon" version="1.0" xmlns="http://www.w3.org/2000/svg" width="1344" height="1344" viewBox="0 0 1008 1008"><path d="M204.2 1.7c-2.7.5-4 2.9-8.7 16.3-15.9 45.8-17.3 93.7-4 140l3.5 12.2-2.2 2.7c-26.9 32.7-40.8 57.1-51.2 90-8.6 27.1-11.1 45.9-11 81.6.1 66.3 10.4 117.2 32.9 163 40.1 81.4 115 127.2 236.5 144.3l18.7 2.7-5.4 6c-6.6 7.2-16.2 21.3-20.9 30.8-5 9.8-10 25.5-12.1 37.7l-1.8 10.5-7.5 3.7c-47.8 23.4-107.5 15.2-147.5-20.4-9.4-8.4-17.6-17.8-23.7-27.4-16.8-26.1-21.5-32.1-33-42.1-18-15.7-42.6-27.6-64.6-31.3-16.7-2.8-34.2 3.1-34.2 11.4 0 6.1 9.2 15.6 26.9 27.8 32.5 22.5 53.9 50.4 66.6 86.8 21.5 61.1 77.5 97 151.2 97 18.7 0 40.4-2.3 60.9-6.5l3.1-.7.6 57.9c.7 62.1.8 62.9 6.2 73.9 3 6.1 10.5 14.8 14.6 16.9 5 2.7 31.2 11.2 42.4 13.8 28.8 6.9 29.4 6.9 85.5 7.4 53.7.5 63.9 0 85.5-3.8 15.7-2.8 28.7-6.2 46.5-12.2 14.7-4.9 15.8-5.4 20.8-10.4 6.7-6.7 11.9-17.3 13.1-26.8.5-3.9 1-46.6 1-95 .1-48.4.4-90.7.7-94 .7-7.1-.8-24.9-3.1-36.1-4.9-24-17.4-49.2-33.8-68.4-3.1-3.5-5.4-6.6-5.2-6.8.2-.2 6.6-1.2 14.3-2.2C791 635.3 866 590 907.1 506.5c16.3-33.3 26.6-73.1 31-120 2.1-21.7 1.8-69.3-.4-83.5-7.2-46.5-24.6-86-53.6-121.8l-9.2-11.3 2.6-8.2c6.8-21.4 10-43.1 9.9-68.2-.1-27.4-3.6-48.5-12.4-73.9C868.4.4 869 1 854.1 1 817.4 1 766 21.2 707.2 58.8l-13.3 8.4-14.7-3.5c-95.7-23.4-192.3-23.4-287.8 0l-15.1 3.7-14.9-9.5C312.1 26.5 270.4 8.4 234 2.5c-8.8-1.4-24.5-1.8-29.8-.8z"/></svg>,
            website: <svg class="website-icon" version="1.0" xmlns="http://www.w3.org/2000/svg" width="1344" height="1344" viewBox="0 0 1100 1008"><path d="M470.5 1.1c-87.1 6.1-170.7 34.2-242.7 81.5C122.1 152.2 46.6 258.1 15.5 380.5c-36.8 144.6-7 299.1 81 419.6 83 113.8 209.2 187.9 347.5 204.3 250.6 29.8 484.6-130.2 548-374.5 11.2-43.3 15.5-78.3 15.5-125.9 0-31.9-.8-43.9-4.6-70.9-13.1-94-53.8-183.8-116.5-257.1-12.6-14.8-39.6-41.8-54.4-54.4C739.1 42.2 622.1-.7 501.2.1c-10.8.1-24.6.5-30.7 1zm44.3 74.5c20.9 10.2 46.9 54.1 65.6 110.7 11.1 33.4 21.8 78.3 27.9 116.9l1.4 8.8H398.3l.3-2.3c4.2-27 11.8-63.2 19-90.1 20.6-77 51.9-134.8 79.1-145.7 6-2.4 10.6-2 18.1 1.7zM390 88.5c0 .3-2.2 5-5 10.5-23.9 47.6-44.7 118.4-56.5 192.8-1.4 8.6-2.8 16.7-3 17.9l-.5 2.3H221.5c-56.9 0-103.5-.3-103.5-.6 0-1.3 8.6-17 16.3-29.9C188.6 191.3 274 124.2 375.5 91.9c11.9-3.8 14.5-4.4 14.5-3.4zm248 5.2c20.2 6.7 34.5 12.5 55.5 22.8 74.8 36.6 137.4 93.9 180.2 165 7.7 12.9 16.3 28.6 16.3 29.9 0 .3-46.6.6-103.5.6H683l-.5-2.3c-.2-1.2-1.6-9.3-3-17.9C667.7 217.4 646.9 146.6 623 99c-2.8-5.5-5-10.2-5-10.6 0-.9 5.4.5 20 5.3zM316.6 389.2c-.9 8.5-2.5 34.5-3.6 58.8-2.2 50-.5 131.4 3.6 170.2l.6 5.8h-228l-2.2-8.1c-9.8-36.5-14.4-71.8-14.4-111.9 0-40.1 4.6-75.4 14.4-111.9l2.2-8.1h228l-.6 5.2zm303.1 9.3c5.1 61.9 5.1 149.1 0 211l-1.2 14h-229l-1.2-14c-3.8-46.4-5-130.5-2.5-174 1.6-26.1 3.2-48.7 3.7-50.3.4-1 23.8-1.2 114.7-1l114.3.3 1.2 14zm301.3-6.4c9.8 36.5 14.4 71.8 14.4 111.9 0 40.1-4.6 75.4-14.4 111.9l-2.2 8.1h-228l.6-5.3c2.4-21.8 4.6-75.1 4.6-114.7 0-39.6-2.2-92.9-4.6-114.8l-.6-5.2h228l2.2 8.1zM325.5 698.2c.2 1.3 1.6 9.4 3 18 11.9 74.5 32.6 145.1 56.6 192.9 2.8 5.6 4.8 10.3 4.5 10.6-.7.7-19.4-5-33.6-10.3-92.6-34.1-171.1-98.9-221.7-182.9-7.7-12.9-16.3-28.6-16.3-29.9 0-.3 46.6-.6 103.5-.6H325l.5 2.2zm283.9 0c-6.4 41.2-17.6 89.2-28.9 123.4-22.4 67.6-53.5 113.9-76.5 113.9-24.6 0-58.3-52.9-80.5-126.5-10.1-33.6-19.3-74.4-24.9-110.8l-.3-2.2h211.4l-.3 2.2zm280.6-1.6c0 1.3-8.6 17-16.3 29.9-50.6 84-129.1 148.8-221.7 182.9-14.2 5.3-32.9 11-33.6 10.3-.3-.3 1.7-5 4.5-10.6 24-47.8 44.7-118.4 56.6-192.9 1.4-8.6 2.8-16.7 3-18l.5-2.2h103.5c56.9 0 103.5.3 103.5.6z"/></svg>
        };
        
        return <a href={link}>
            {platforms[platform]}
        </a> 
    }

    const profiles = [
        {
            display: "https://raw.githubusercontent.com/08Aristodemus24/eda-denoiser-stress-detector/master/client-side/src/assets/mediafiles/profiles/christaline.png",
            name: "Christaline Calubayan", 
            role: "Associate AI/ML Researcher & Documentation", 
            // mobile_num: "(+63) 970 745 1021", 
            socials: {
                linkedin: "https://www.linkedin.com/in/christaline-calubayan-01127b262/",
                facebook: "https://www.facebook.com/cchrstln",
                github: "https://github.com/cchrxstln"
            }
        },
        {
            display: "https://raw.githubusercontent.com/08Aristodemus24/eda-denoiser-stress-detector/master/client-side/src/assets/mediafiles/profiles/deseree.jpg",
            name: "Deseree Quiray", 
            role: "AI/ML Researcher, Public Relations, and Logistics", 
            // mobile_num: "(+63) 970 745 1021", 
            socials: {
                linkedin: "https://www.linkedin.com/in/deseree-quiray-7b6a74330",
                facebook: "https://www.facebook.com/deseree.quiray",
            }
        },
        {
            display: "https://raw.githubusercontent.com/08Aristodemus24/eda-denoiser-stress-detector/master/client-side/src/assets/mediafiles/profiles/johana.jpg",
            name: "Johana Benolirao", 
            role: "Graphic Designer, AI/ML Researcher, and Public Relations", 
            // mobile_num: "(+63) 970 745 1021", 
            socials: {
                linkedin: "https://www.linkedin.com/in/johana-benolirao-8902172ba",
                facebook: "https://www.facebook.com/iamwana18",
            }
        },
        {
            display: "https://raw.githubusercontent.com/08Aristodemus24/eda-denoiser-stress-detector/master/client-side/src/assets/mediafiles/profiles/larry.jpg",
            name: "Larry Miguel R. Cueva", 
            role: "Lead AI/ML Engineer & Researcher", 
            mobile_num: "(+63) 970 745 1021", 
            socials: {
                linkedin: "https://www.linkedin.com/in/michaelcueva/",
                facebook: "https://fb.com/mig.cueva.7",
                github: "https://github.com/08Aristodemus24",
                website: "https://project-alexander.vercel.app/"
            }
        },
    ]

    const researcher_items = profiles.map((profile, index) => {
        return (
            <div className="researcher-item" key={index}>
                <div className="researcher-content">
                    <h3 className="researcher-name">{profile["name"]}</h3>
                    <p className="researcher-role">{profile["role"]}</p>
                    <p className="researcher-mobile-num">{!profile["mobile_num"] ? "-" : profile["mobile_num"]}</p>
                    <div className="researcher-socials">
                        {Object.entries(profile["socials"]).map((social, index) => {
                            // social contains the key and value pair representing 
                            // the platform and corresponding link to that researchers 
                            // social media platform
                            const [platform, link] = social;
                            const svgs = getSvgs({ platform, link });

                            // return anchor tag containing the svg
                            return svgs;
                        })}
                    </div>
                </div>
                <img className="researcher-img" src={profile['display']} alt="" srcset="" />
            </div>
        )
    })

    return (
        <Section section-name={"researchers"}>
            <h1 className="researchers-header">Researchers</h1>
            <div className="researchers-info">
                {researcher_items}
            </div>
        </Section>
    )
}