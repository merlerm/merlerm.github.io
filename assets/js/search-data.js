// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-publications",
          title: "publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-now",
          title: "now",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/now/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-contact",
          title: "contact",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/contact/";
          },
        },{id: "post-looking-back-at-two-years-in-finland",
        
          title: "Looking Back at Two Years in Finland",
        
        description: "A reflection on my time pursuing my Master&#39;s degree at Aalto University in Helsinki.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/finland-retrospective/";
          
        },
      },{id: "news-our-paper-in-context-symbolic-regression-leveraging-large-language-models-for-function-discovery-has-been-accepted-at-the-acl-2024-student-research-workshop",
          title: 'Our paper “In-Context Symbolic Regression: Leveraging Large Language Models for Function Discovery” has...',
          description: "",
          section: "News",},{id: "news-our-paper-generating-code-world-models-with-large-language-models-guided-by-monte-carlo-tree-search-has-been-accepted-at-neurips-2024",
          title: 'Our paper “Generating Code World Models with Large Language Models Guided by Monte...',
          description: "",
          section: "News",},{id: "news-my-master-s-thesis-was-awarded-as-one-of-the-three-best-at-the-aalto-university-school-of-science-in-2024",
          title: 'My Master’s Thesis was awarded as one of the three best at the...',
          description: "",
          section: "News",},{id: "news-we-released-a-new-preprint-viplan-a-benchmark-for-visual-planning-with-symbolic-predicates-and-vision-language-models",
          title: 'We released a new preprint: ViPlan: A Benchmark for Visual Planning with Symbolic...',
          description: "",
          section: "News",},{id: "news-a-preliminary-version-of-our-latest-work-guiding-reinforcement-learning-with-selective-vision-language-model-supervision-has-been-published-in-the-ecai-2025-caipi-workshop-we-are-currently-extending-this-work-into-a-full-length-paper-for-a-conference-submission",
          title: 'A preliminary version of our latest work, Guiding Reinforcement Learning with Selective Vision-Language...',
          description: "",
          section: "News",},{id: "news-we-released-a-new-preprint-decselfmask-leveraging-unlabeled-text-via-self-relevance-guided-masking-for-decoder-only-classification-led-by-pietro-ferrazzi",
          title: 'We released a new preprint: DecSelfMask: Leveraging Unlabeled Text via Self-Relevance-Guided Masking for...',
          description: "",
          section: "News",},{id: "news-we-released-a-new-preprint-qval-cheaply-evaluating-dense-supervision-signals-for-long-horizon-llm-agents-led-by-sergio-hernández",
          title: 'We released a new preprint: QVal: Cheaply Evaluating Dense Supervision Signals for Long-Horizon...',
          description: "",
          section: "News",},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%6D%6D%65%72%6C%65%72@%66%62%6B.%65%75", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/merlerm", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/merlerm", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=2_dW7y4AAAAJ", "_blank");
        },
      },{
        id: 'social-x',
        title: 'X',
        section: 'Socials',
        handler: () => {
          window.open("https://twitter.com/merler_m", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
