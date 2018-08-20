import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette(sns.color_palette(palette = 'bright', n_colors = 6))

THEME = {'Science &\nPolicy': 21,
        'Science &\nSociety': 25,
        'Science, Innovation, &\nEconomic Development': 15,
        'Science &\nInternational\nAffairs': 3,
        'Science\n& the Next\nGeneration': 11}

FORMAT = {'Green\nPaper': 10,
        'Case\nStudies': 10,
        'Short\nTalks': 8,
        'Interactive\nSessions': 7,
        'Debates': 3,
        'Panels': 37}

SECTOR = {'Government': 16,
        'Academia': 16,
        'Private\nSector': 6,
        'Non-profit': 37}

for d, file in zip([THEME, FORMAT, SECTOR], ['By_Theme', 'By_Format', 'By_Sector']):
    fig, ax = plt.subplots(figsize = (6, 6))
    k, v, e = [k for k in d.keys()], [v for v in d.values()], [0.02 for _ in d.keys()]
    p, t, at = ax.pie(v, labels = k, explode = e, autopct = '%1f', wedgeprops = {'lw': 0.75,
        'ec': '#333333', 'alpha': 0.95})
    ax.set_title('Breakdown ' + file.replace('_', ' '))

    for i,T in enumerate(at):
        T.set_text(str(v[i]))
        T.set_color('w')
        
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    plt.savefig('PanelSubmissions' + file.replace('_', '') + '.png', dpi = 300)
    plt.clf()
    plt.close()
