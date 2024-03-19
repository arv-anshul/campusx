# DSMP by CampusX

<p align="center">
  <a href="https://learnwith.campusx.in" title="Go to Website">
    <img src="https://avatars.githubusercontent.com/u/53361867?v=4" style="width: 200px; border-radius: 50%;" />
  </a>

  <h3 align="center">DSMP By <a href="https://learnwith.campusx.in">CampusX</a></h3>
  <p align="center">
    Here, you can get all the resources like <strong>🔗 Links of 📝 Notes and 📓 Notebooks</strong> provided in the DSMP Course.
  </p>

  <p align="center">
  <strong>Author:</strong> <a href="https://github.com/arv-anshul">Anshul Raj Verma</a>
  </p>

</p>

<p align="center">
  <a href="https://youtube.com/@campusx-official" title="CampusX YouTube Channel">
    <img src="https://img.shields.io/badge/CampusX-F00?logo=youtube&logoColor=fff" alt="CampusX YouTube Channel">
  </a>
  <a href="https://learnwith.campusx.in" title="CampusX DSMP Website">
    <img src="https://img.shields.io/badge/CampusX_DSMP-0056D2?logo=curl&logoColor=fff" alt="CampusX DSMP Website">
  </a>
  </br>
  <a href="https://squidfunk.github.io/mkdocs-material/" title="Built with Material for MkDocs">
    <img src="https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white" alt="Built with Material for MkDocs">
  </a>
  <a href="https://arv-anshul.github.io/campusx-dsmp" title="Hosted with GitHub Pages">
    <img src="https://img.shields.io/badge/GitHub%20Pages-222?logo=github&logoColor=fff" alt="GitHub Badge">
  </a>
  <a href="https://github.com/arv-anshul/campusx-dsmp/actions" title="Build and Deploy with GitHub Actions">
    <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=fff" alt="GitHub Actions Badge">
  </a>
  <a href="https://rye-up.com" title="Project Management Tool">
    <img src="https://img.shields.io/badge/Rye-000?logo=rye&logoColor=fff" alt="Rye Badge">
  </a>
</p>

> \[!WARNING\]
>
> The listed resource is not suitable for the **Unpaid/Free User (who have not bought the course)** because it **only consists the paid lecture's notes and links** which are provided in the description **by The Mentor**.

### 🙌 Praise for this Project

<p align="center">

https://github.com/arv-anshul/campusx-dsmp/assets/111767754/3414dc8e-d474-4751-b504-317d7d719d3e

</p>

### ♻️ Project Workflows

1. **Data Collection:** Gathered data from the HTML structure of the course's website.
2. **Script Development:** Developed Python scripts responsible for parsing HTML and extracting essential data required for subsequent requests.
3. **HTTP Requests:** Performed a series of Http GET requests to the website to obtain session resources, particularly video sessions in the current implementation.
4. **Testing:** Implemented a suite of tests for the [`course_parser.py`](./src/course_parser.py) script to ensure robust and reliable HTML parsing.
5. **Data Structure Maintenance:** Maintained the integrity and structure of the acquired data and resources, ensuring they are ready for presentation on a web page.
6. **Documentation and Presentation:** Utilized `mkdocs` along with the `mkdocs-material` theme/extension to seamlessly generate a professional-looking web page.
7. **Continuous Integration and Deployment (CI/CD):** Employed **Github Actions** to automate the build and deployment processes, ensuring the web page is always up-to-date.
8. **Web Hosting:** Leveraged **Github Pages** as a reliable hosting solution to make the web page accessible to a wider audience.

By following these workflows, the project ensures efficient data extraction, robust testing, proper documentation, and automated deployment, ultimately resulting in a well-maintained and accessible web page hosted on Github Pages.

## Downloaded Resources

🥳 You can get all the course's resources like `.pdf`, `.ipynb`, `.docx`, `.pptx`, `.xlsx` and `.py` files in 🗂️ [`resources`](./resources/) directory.

> \[!CAUTION\]
>
> If you get any problem while opening a file then try to change its file extension. My program is not good at inferring file extension 😞. Otherwise, [raise issue](https://github.com/arv-anshul/campusx-dsmp/issues).

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

## ⚙️ Project Setup

1. Clone the repository.

```bash
git clone https://github.com/arv-anshul/campusx-dsmp
```

2. This project is managed using [`rye`](https://rye-up.com). So, install it using:

```bash
curl -sSf https://rye-up.com/get | bash
```

3. Rename `example.env` to `.env` and define the required environment variables.

<details>
<summary>🔥 Prerequisites</summary>

1. You have to purchase the course.
2. Open the course's website and developer tools of browser.
3. Go to Networks Tab.
4. Select the request where the website makes a call for the data to display.
   - In the "Networks" tab, find the request that corresponds to the data retrieval call. You may filter the requests by XHR or fetch type for AJAX requests.
   - Look for the request URL related to fetching data or making an API call.
5. Copy `c_ujwt` and `SESSIONID` values from the `cookies` headers of that request.
   - Within the selected request, locate the "Headers" tab.
   - Look for the "Cookies" section under "Request Headers" or "Response Headers."
   - Copy the values of `c_ujwt` and `SESSIONID`. These are essential for authenticating your requests.

</details>

```toml
# Define these to construct cookies for making requests
C_UJWT=""
SESSION_ID=""
```

4. If you want to fetch resources from the website then run the `main.py` script. I have written all the steps to fetch the resources of the sub-topics.

> You can configure the `main.py` to fetch different type of resources like `"video", "assignment"`.

```bash
rye run fetch
```

### Issues

If you have any issue or query related to this project you can raise [here](https://github.com/arv-anshul/campusx-dsmp/issues "Project's Issues Tab").
