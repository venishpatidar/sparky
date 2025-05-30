const fs = require("fs");

const BASE_URL =
  "https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/";
const RAW_DATA = "raw_data";
const CLASS_FOLDER_NAME = "classes";
let CLASS_FILE_COUNTER = 0;

const classFolderPath = `${RAW_DATA}/${CLASS_FOLDER_NAME}`;
if (!fs.existsSync(classFolderPath)) {
  fs.mkdirSync(classFolderPath, { recursive: true });
}

const DEFAULT_FILTER = {
  refine: "Y",
  campusOrOnlineSelection: "A",
  honors: "F",
  promod: "F",
  searchType: "all",
  term: "2251",
  scrollId: "",
};

const parseURL = (filter = DEFAULT_FILTER) => {
  const {
    refine,
    campusOrOnlineSelection,
    honors,
    promod,
    searchType,
    term,
    scrollId,
  } = filter;
  return (
    BASE_URL +
    "classes?" +
    `&refine=${refine}&campusOrOnlineSelection=${campusOrOnlineSelection}&honors=${honors}&promod=${promod}&searchType=${searchType}&term=${term}&scrollId=${scrollId}`
  );
};

async function fetchClasses(term = "2251", scrollID = "", totalClass = 0) {
  const filter = DEFAULT_FILTER;
  filter.scrollId = scrollID;
  filter.term = term;
  // console.log(`URL: ${parseURL(filter)}`);
  const response = await fetch(parseURL(filter), {
    cache: "default",
    credentials: "include",
    headers: {
      Accept: "*/*",
      "Accept-Language": "en-US,en;q=0.9",
      Authorization: "Bearer null", //If removed gives unauthorized access
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    },
    method: "GET",
    mode: "cors",
    redirect: "follow",
    referrer: "https://catalog.apps.asu.edu/",
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let allChunks = "";
  let { done, value } = await reader.read();
  while (!done) {
    allChunks += decoder.decode(value, { stream: true });
    const rs = await reader.read();
    done = rs.done;
    value = rs.value;
  }

  const JSON_OBJ = JSON.parse(allChunks);

  if (JSON_OBJ.classes.length !== 0) {
    fs.writeFile(
      `${classFolderPath}/classes_${CLASS_FILE_COUNTER}.json`,
      JSON.stringify(JSON_OBJ),
      (err) => {
        if (err) console.log(err);
      },
    );
    CLASS_FILE_COUNTER += 1;

    fetchClasses(
      (term = "2251"),
      (scrollID = JSON_OBJ.scrollId),
      (totalClass = totalClass + JSON_OBJ.classes.length),
    );
  } else {
    console.log(
      `Total Classes retrived ${totalClass} in ${CLASS_FILE_COUNTER} files.`,
    );
    CLASS_FILE_COUNTER = 0;
  }
}

async function fetchCourseDescr(params) {
  const { course_id, term, subject, catalogNbr } = params;
  const response = await fetch(
    BASE_URL +
      `courses?refine=Y&catalogNbr=${catalogNbr}&course_id=${course_id}&subject=${subject}&term=${term}`,
    {
      cache: "default",
      credentials: "include",
      headers: {
        Accept: "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        Authorization: "Bearer null", //If removed gives unauthorized access
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
      },
      method: "GET",
      mode: "cors",
      redirect: "follow",
      referrer: "https://catalog.apps.asu.edu/",
    },
  );

  //Creating reader stream
  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let allChunks = "";
  let { done, value } = await reader.read();
  while (!done) {
    allChunks += decoder.decode(value, { stream: true });
    const rs = await reader.read();
    done = rs.done;
    value = rs.value;
  }
  const JSON_OBJ = JSON.parse(allChunks)[0];
  if (require.main !== module) {
    console.log(JSON_OBJ.DESCRLONG ? JSON_OBJ.DESCRLONG : "");
  }
  return JSON_OBJ.DESCRLONG ? JSON_OBJ.DESCRLONG : "";
}

if (require.main === module) {
  // This code will be executed when the script is run directly
  fetchClasses();
} else {
  // Code to be executed when the script is imported as a module
  module.exports = { fetchCourseDescr };
}
