# CampusX Course Resources

<p align="center">
  <a href="https://learnwith.campusx.in">
    <img src="https://avatars.githubusercontent.com/u/53361867?v=4" style="width: 200px; border-radius: 50%;" />
  </a>

  <h3 align="center">CampusX Course Resources</h3>
  <p align="center">
    Here, you can get all the resources like Notes and Notebooks provided in CampusX Courses.
    <br>
    <strong>By <a href="https://github.com/arv-anshul">Anshul Raj Verma</a></strong>
  </p>
</p>

<p align="center">
  <a href="https://youtube.com/@campusx-official" title="CampusX YouTube Channel">
    <img src="https://img.shields.io/badge/CampusX-F00?logo=youtube&logoColor=fff" alt="CampusX YouTube Channel">
  </a>
  <a href="https://learnwith.campusx.in" title="CampusX DSMP Website">
    <img src="https://img.shields.io/badge/CampusX_DSMP-0056D2?logo=curl&logoColor=fff" alt="CampusX DSMP Website">
  </a>
  <br>
  <img src="https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white" alt="Built with Material for MkDocs">
  <img src="https://img.shields.io/badge/GitHub%20Pages-222?logo=github&logoColor=fff" alt="GitHub Badge">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=fff" alt="GitHub Actions Badge">
  <img src="https://img.shields.io/badge/Rye-000?logo=rye&logoColor=fff" alt="Rye Badge">
</p>

### 🙌 Praise for this Project

<p align="center">

https://github.com/arv-anshul/campusx/assets/111767754/3414dc8e-d474-4751-b504-317d7d719d3e

</p>

### ♻️ Project Workflows

1. **Data Collection:** Gathered data from the HTML structure of the course's website.
2. **Script Development:** Developed Python scripts responsible for parsing HTML and extracting essential data required for subsequent requests.
3. **HTTP Requests:** Performed a series of Http GET requests to the website to obtain session resources, particularly video sessions in the current implementation.
4. **Testing:** Implemented a suite of tests for the [`course_parser.py`](./src/dsmp2/course_parser.py) script to ensure robust and reliable HTML parsing.
5. **Data Structure Maintenance:** Maintained the integrity and structure of the acquired data and resources, ensuring they are ready for presentation on a web page.
6. **Documentation and Presentation:** Utilized `mkdocs` along with the `mkdocs-material` theme/extension to seamlessly generate a professional-looking web page.
7. **Continuous Integration and Deployment (CI/CD):** Employed **Github Actions** to automate the build and deployment processes, ensuring the web page is always up-to-date.
8. **Web Hosting:** Leveraged **Github Pages** as a reliable hosting solution to make the web page accessible to a wider audience.

By following these workflows, the project ensures efficient data extraction, robust testing, proper documentation, and automated deployment, ultimately resulting in a well-maintained and accessible web page hosted on Github Pages.

## Downloaded Resources

🥳 You can get all the course's resources like `.pdf`, `.ipynb`, `.docx`, `.pptx`, `.xlsx` and `.py` files in 🗂️ [`resources`](./resources/) directory.

> \[!CAUTION\]
>
> If you get any problem while opening a file then try to change its file extension. My program is not good at inferring file extension 😞. Otherwise, [raise issue](https://github.com/arv-anshul/campusx/issues).

<details>
<summary>Resources File Structure</summary>

```bash
./resources
├── README.md
├── DSMP
│   ├── Parent Session1
│   │   ├── Lecture1
│   │   │   ├── Resource1
│   │   │   └── Resource2
│   │   └── Lecture2
│   │       ├── Resource1
│   │       └── Resource2
│   └── Parent Session2
│       └── Lecture1
│           ├── Resource1
│           └── Resource2
└── Extra  # Some extra stuffs from course (added manually)
```

</details>

### Issues

If you have any issue or query related to this project you can raise [here](https://github.com/arv-anshul/campusx/issues "Project's Issues Tab").
