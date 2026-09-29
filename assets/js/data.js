/* ==========================================================================
   picoGIGA Lab — site content
   Edit this file to update members, publications and news.
   Every page reads from here, so there is no build step.
   ========================================================================== */

window.LAB = {
  name: "picoGIGA Lab",
  fullName: "pico-to-GIGA Multiscale Simulation Research Group",
  institute: "Clean Energy Research Center, Korea Institute of Science and Technology (KIST)",
  address: "5 Hwarang-ro 14-gil, Seongbuk-gu, Seoul, Republic of Korea",
  email: "kyeongsu@kist.re.kr"
};

/* --------------------------------------------------------------------------
   PEOPLE
   areas: research areas of the member (co2, biomass, plastic, dft, ml, process).
   Every paper or patent a member co-authors is filed under these areas automatically.
   photo: path under assets/img/people/. If the file is missing, initials are shown.
   -------------------------------------------------------------------------- */
window.PI = {
  name: "Kyeongsu Kim",
  ko: "김경수",
  title: "Senior Research Scientist",
  affiliation: "Clean Energy Research Center, KIST",
  email: "kyeongsu@kist.re.kr",
  photo: "assets/img/people/kim-kyeongsu.jpg",
  summary:
    "Simulation studies for CO₂ capture and conversion (CCUS), direct air capture (DAC), biomass energy and plastic upcycling.",
  career: [
    { period: "Present", role: "Senior Research Scientist", place: "Clean Energy Research Center, KIST" },
    { period: "2019 – 2021", role: "Postdoctoral Researcher", place: "Korea Institute of Science and Technology", note: "System engineering and computational science for CO₂ conversion" },
    { period: "2019", role: "Ph.D. in Engineering", place: "Chemical & Biological Engineering, Seoul National University", note: "Process systems engineering and optimization" },
    { period: "2013", role: "B.S.", place: "Chemical & Biological Engineering, Seoul National University" }
  ]
};

window.MEMBERS = [
  {
    group: "Postdoctoral Researchers",
    people: [
      { name: "Eugene Huh", areas: ["dft"], ko: "허유진", photo: "huh-eugene.jpg", interests: ["DFT and MD simulation", "CO₂ conversion"], email: "eugeneh55@gmail.com" },
      { name: "Hyein Jung", areas: ["process", "ml"], ko: "정혜인", photo: "jung-hyein.jpg", interests: ["Process design and analysis", "ML/DL for chemical process"], email: "1300hannah@gmail.com" },
      { name: "Wonyoung Choi", areas: ["ml"], ko: "최원영", photo: "choi-wonyoung.jpg", interests: ["AI-based knowledge structuring"], email: "wychoi1020@kist.re.kr" },
      { name: "A Ra Cho", areas: ["dft", "ml"], ko: "조아라", photo: "cho-ara.jpg", interests: ["DFT", "MLIP"], email: "orzr03@kist.re.kr" }
    ]
  },
  {
    group: "Graduate Students",
    people: [
      { name: "Muhammad Ramadhan", areas: ["dft"], ko: "라마단", role: "Ph.D. candidate", photo: "ramadhan.jpg", interests: ["Homogeneous/heterogeneous catalysis", "DFT simulation"], email: "ramadhankr@kist.re.kr" },
      { name: "Nurul Fuadi P.S.", areas: ["process"], ko: "누룰", role: "Ph.D. candidate", photo: "nurul.jpg", interests: ["Process engineering", "Chemical process modeling"], email: "nurulfuadips@kist.re.kr" },
      { name: "So Hui Park", areas: ["dft", "ml"], ko: "박소희", role: "M.S. candidate", photo: "park-sohui.jpg", email: "t260062@kist.re.kr" }
    ]
  },
  {
    group: "Guest Member",
    people: [
      { name: "Jeong Hun Kim", areas: ["dft"], ko: "김정훈", role: "Ph.D. candidate", photo: "kim-jeonghun.jpg", interests: ["Heterogeneous catalysis experiment", "DFT simulation"], email: "shining_lune@kist.re.kr" }
    ]
  },
  {
    group: "Interns",
    people: [
      { name: "Yae Chan Park", areas: ["process"], ko: "박예찬", role: "Intern", photo: "park-yaechan.jpg", interests: ["Process engineering", "Kinetic modeling"], email: "parkerbros@kist.re.kr" }
    ]
  }
];

/* Alumni: former members and where they are now. Newest first. Leave "now" empty if unknown. */
window.ALUMNI = [
  { name: "Suk Hoon Choi", areas: ["ml"], ko: "최석훈", was: "Postdoctoral researcher", now: "SK innovation" },
  { name: "Hyerim Kim", areas: ["process"], ko: "김혜림", was: "Postdoctoral researcher", now: "Korea Institute of Machinery & Materials (KIMM)" },
  { name: "Nayoun Park", areas: ["process"], ko: "박나연", was: "M.S. student", now: "Henkel Korea" },
  { name: "Tae Ung Lee", areas: [], ko: "이태웅", was: "Undergraduate intern", now: "Graduate student, KAIST" },
  { name: "Seo Eun Lee", areas: [], ko: "이서은", was: "Undergraduate intern", now: "" }
];

/* Group photos, NEWEST FIRST. The home page shows the first one that exists. */
window.GROUP_PHOTOS = [
  { src: "assets/img/group/2026-06.jpg", caption: "June 2026" },
  { src: "assets/img/group/2026-04.jpg", caption: "April 2026" },
  { src: "assets/img/group/2025-09.jpg", caption: "September 2025" },
  { src: "assets/img/group/2025-06.jpg", caption: "June 2025" },
  { src: "assets/img/group/2025-04.jpg", caption: "April 2025" },
  { src: "assets/img/group/2023-04.jpg", caption: "April 2023" },
  { src: "assets/img/group/2023-01.jpg", caption: "January 2023" }
];

/* Publications live in publications.js, generated from Google Scholar by
   tools/sync_publications.py. Corrections go in tools/publication_overrides.json. */

/* --------------------------------------------------------------------------
   NEWS
   Newest first. img: path under assets/img/news/ (optional).
   -------------------------------------------------------------------------- */
window.NEWS = [
  { y: 2025, title: "2025 AIChE Annual Meeting", img: "n02.jpg" },
  { y: 2025, title: "2025 AIChE Annual Meeting", text: "Oral presentation by Dr. 최석훈", img: "n03.jpg" },
  { y: 2025, title: "2025 AIChE Annual Meeting", text: "Oral presentation by 박나연", img: "n04.jpg" },
  { y: 2025, title: "KIST Sports Day, Fall 2025", img: "n05.jpg" },
  { y: 2025, title: "KIST Sports Day, Spring 2025", img: "n06.jpg" },
  { y: 2025, title: "Turbo Expo 2025, Memphis, Tennessee, USA", text: "Oral presentation by Dr. 김혜림", img: "n07.jpg" },
  { y: 2025, title: "공업화학회 단체사진", text: "(함정 있음)", img: "n08.jpg" },
  { y: 2025, title: "미원상사 신진과학자 포럼", text: "Dr. 김", img: "n09.jpg" },
  { y: 2025, title: "구두발표", text: "라마", img: "n10.jpg" },
  { y: 2025, title: "포스터발표", text: "나연", img: "n11.jpg" },
  { y: 2025, title: "봄 한국화학공학회", text: "신진연구자 발표", img: "n12.jpg" },
  { y: 2025, title: "스승의 날 행사", text: "논문 ‘많이’ 쓸게요!", img: "n13.jpg" },
  { y: 2025, title: "Seminar by Prof. G. K. Surya Prakash", text: "A Carbon Solution to the Carbon Problem: The Methanol Economy", img: "n14.jpg" },

  { y: 2024, title: "2024 KIChE Conference", text: "놀러간 거 아님. 발표도 했음.", img: "n15.jpg" },
  { y: 2024, title: "2022 AIChE Annual Meeting", text: "놀러간 거 아님. 발표도 했음.", img: "n16.jpg" },
  { y: 2024, title: "2024 KIChE Conference", text: "이산화탄소 연구 발표함. 나름 잘했음", img: "n17.jpg" },
  { y: 2024, title: "Turbo Expo 2024, London, UK", text: "Oral presentation by Dr. 김혜림", img: "n18.jpg" },
  { y: 2024, title: "2024 AIChE Annual Meeting", img: "n19.jpg" },
  { y: 2024, title: "삼총사", img: "n20.jpg" },
  { y: 2024, title: "이래봬도 발전 중", img: "n21.jpg" },
  { y: 2024, title: "첫 발표라 뻘쭘", img: "n22.jpg" },
  { y: 2024, title: "위아래 위위아래", img: "n23.jpg" }
];
