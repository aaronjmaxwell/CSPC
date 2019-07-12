panel = dict(
    NSERC_CRSNG = "Mapping Dynamic Research Ecosystems",
    e4dca = "Evidence in Practice",
    kimberlygirling = "Evidence in Practice",
    KarenAkerlof = "Evidence in Practice",
    tedhsu = "Evidence in Practice",
    NRCan = "Bringing the Social Sciences Into New Policy Spaces",
    _LMS_adm = "Bringing the Social Sciences Into New Policy Spaces",
    RNCan = "Bringing the Social Sciences Into New Policy Spaces",
    _STM_sma = "Bringing the Social Sciences Into New Policy Spaces",
)

# remove having to check for upper and lower case letters, since Twitter is case insensitive.
panel = {k.lower(): v for k, v in panel.items()}
