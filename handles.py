panel = dict(
    # Multiples
    SSHRC_CRSH = ["Informing Policy by Leveraging Knowledge", # Rebecca
                "Granting Agencies and Participatory Science in Canada"], # Greg
    NSERC_CRSNG = ["Shaping Science Policy to Improve Equity, Diversity and Inclusion", # Jennifer
        "Granting Agencies and Participatory Science in Canada"], # Greg
    NRCan = ["Canada's Climate Change Adaptation Platform",
        "From AI to Policy (Map-)Making"], # Aaron
    OntScienceCtr = ["Breaking the Habit", # Aaron
                    "The Status of Science Literacy in Canada"], # Greg
    Sofia_Barrows = ["Breaking the Habit", # Aaron
        "Equity, Diversity and Inclusion in Science"],
    # Rebecca
    CollegeCan = "Incorporating Indigenous Ways of Knowing",
    INFC_eng = "Informing Policy by Leveraging Knowledge",
    Eleanor_Fast = "The Dementia Challenge",
    CAHS_ACSS = "The Dementia Challenge",
    #  Aaron
    allouttalemons = "Breaking the Habit",
    Scienceadvice = "Failure to Thrive",
    emmeslin = "Failure to Thrive",
    OCEinnovation = "Commercializing Innovation in Canada",
    BMSchmidt = "Canada 2067",
    LetsTalkScience = "Canada 2067",
    # Cat
    E4Dca = "Integrating Indigenous Knowledge and Western Science",
    LiberEroFellows = "Integrating Indigenous Knowledge and Western Science",
    litscientist = "Improvisation for Science Communication",
    pixelsandplans = "Innovating Science Communication",
    WWFCanada = "Fueling Water Innovation in Atlantic Canada",
    # Jennifer
    SFU_Water = "Brainstorming for Canada’s National Water Vision",
    RyUrbanWater = "Brainstorming for Canada’s National Water Vision",
    NicH2Olas = "Brainstorming for Canada’s National Water Vision",
    Zafar_Adeel_ = "Brainstorming for Canada’s National Water Vision",
    RySciDean = "Equity, Diversity and Inclusion in Science",
    RyersonU = "Equity, Diversity and Inclusion in Science",
    fanny_eugene = "Shaping Science Policy to Improve Equity, Diversity and Inclusion",
    maryrosebgill = "Shaping Science Policy to Improve Equity, Diversity and Inclusion",
    Diversity_Blog = "Shaping Science Policy to Improve Equity, Diversity and Inclusion",
    aaas = "Shaping Science Policy to Improve Equity, Diversity and Inclusion",
    FRQ_NT = "Shaping Science Policy to Improve Equity, Diversity and Inclusion",
    # Greg
    MitacsCanada = "Risk Communication and Engagement with the Public",
    AKillikelly = "Risk Communication and Engagement with the Public",
    Maurice_Bitran = "The Status of Science Literacy in Canada",
    SciChefQC = "Granting Agencies and Participatory Science in Canada",
    SciChefCan = "Granting Agencies and Participatory Science in Canada",
    MollyShoichet = "Granting Agencies and Participatory Science in Canada",
    CIHR_IRSC = "Granting Agencies and Participatory Science in Canada",
    Joe_S_Sparling = "Where the Rubber Meets the Road",
    CAPSACSP = "Where the Rubber Meets the Road",
    # Conor
    m_m_campbell = "Science Based Policies to Address new Agri-Food Realities",
    uofg = "Science Based Policies to Address new Agri-Food Realities",
    SilkeNebel = "Connecting Science with Policy in Canada",
    Science2Action = "Connecting Science with Policy in Canada",
    WillemseLA = "Fake News, Fake Therapies",
    StemCellNetwork = "Fake News, Fake Therapies",
    # Rhiannon
    AlyssaDaku = "Should science-based Organizations Define their Risk Tolerances",
    CFIA_Canada = "Should science-based Organizations Define their Risk Tolerances",
    #BCHealth = "Putting Our Minds Together",
    itsinyoutogive = "From Crisis to Confidence",
    DrDanaDevine = "From Crisis to Confidence")
# remove having to check for upper and lower case letters, since Twitter is case insensitive.
panel = {k.lower(): v for k, v in panel.items()}
