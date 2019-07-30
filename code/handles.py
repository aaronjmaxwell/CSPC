panel = dict(
    NSERC_CRSNG = ["Mapping Dynamic Research Ecosystems", "Fishing for Open Science Innovation"],
    CRSNG_NSERC  = ["Mapping Dynamic Research Ecosystems", "Fishing for Open Science Innovation"],
    CIHR_IRSC = "Fishing for Open Science Innovation",
    IRSC_CIHR = "Fishing for Open Science Innovation",
    SSHRC_CRSH = ["Fishing for Open Science Innovation",
                  "Interdisciplinary Artificial Intelligence"],
    CRSH_SSHRC = ["Fishing for Open Science Innovation",
                  "Interdisciplinary Artificial Intelligence"],
    e4dca = "Evidence in Practice",
    kimberlygirling = "Evidence in Practice",
    KarenAkerlof = "Evidence in Practice",
    tedhsu = "Evidence in Practice",
    NRCan = "Bringing the Social Sciences Into New Policy Spaces",
    _LMS_adm = "Bringing the Social Sciences Into New Policy Spaces",
    RNCan = "Bringing the Social Sciences Into New Policy Spaces",
    _STM_sma = "Bringing the Social Sciences Into New Policy Spaces",
    SFU = ["Precision Policy", "Interdisciplinary Artificial Intelligence"],
    AB_Enviro = "The Public Record",
    SciChefQC = "The Public Record",
    katiegibbs = "The Public Record",
    ESRC = "Interdisciplinary Artificial Intelligence",
    CukierWendy = "Supports for Women Entrepreneurs",
    RyersonDI = "Supports for Women Entrepreneurs",
    ISSP_uOttawa = "Whose Facts Actually Matter?",
    IOGca = "Whose Facts Actually Matter?",
    Carleton_U = "Why pro-LGBT policies can turn out to be Innovation policies?",
    EU_ScienceHub = "The Sciences of Human Behaviour",
    yuliakrolik = "Creating SciComm",
    pixelsandplans = "Creating SciComm",
    artthescience = "Creating SciComm",
    saraheverts = "Fighting the Opioid Crisis",
    JSchool_CU = "Fighting the Opioid Crisis",
    CSIP_JSGS = "Risk, Uncertainty, Unknowns, and Nonsense",
    JSGSPP = "Risk, Uncertainty, Unknowns, and Nonsense",
    thefathomfund = "Harnessing the Power of the Crowd",
    MEOPAR_NCE = "Harnessing the Power of the Crowd",
    TheNeuro_MNI = "Open Science is Transforming the Research Landscape",
)

# remove having to check for upper and lower case letters, since Twitter is case insensitive.
panel = {k.lower(): v for k, v in panel.items()}
