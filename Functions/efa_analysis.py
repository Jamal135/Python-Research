''' Creation Date: 24/11/2022 '''


import re
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from factor_analyzer import FactorAnalyzer
import matplotlib as plt
import matplotlib.pyplot as pylt
import numpy
import inquirer


try:
    import Functions.library as lib
except ImportError:
    import library as lib


METHODS = {
    'Principal Axis Factoring': 'principal',
    'Maximum Likelihood': 'ml',
    'Minimum Residual': 'minres'
    }
ROTATIONS = {
    'Varimax': 'varimax', 
    'Promax': 'promax', 
    'Oblimin': 'oblimin', 
    'Oblimax': 'oblimax', 
    'Quartimin': 'quartimin', 
    'Quartimax': 'quartimax', 
    'Equamax': 'equamax', 
    'Geomin Oblique': 'geomin_obl', 
    'Geomin Orthogonal': 'geomin_ort'
    }


class EFA_Settings:
    ''' Purpose: Constructs class storing EFA settings. '''
    def __init__(self):
        datafiles = lib.get_files(lib.DATAFOLDER, '.csv')
        self.datafile = lib.get_choice(datafiles, 'Please select a CSV for analysis')
        ''' Contains: selected CSV data file name.'''
        self.dataframe = lib.get_CSV(self.datafile)
        ''' Contains: Dataframe of loaded CSV contents. '''
        self.method = lib.get_choice(METHODS, 'Please select the EFA method')
        ''' Contains: User selected EFA method. '''
        self.rotation = lib.get_choice(ROTATIONS, 'Please select EFA rotation')
        ''' Contains: User selected EFA rotation. '''
        self.topics = len(self.dataframe.columns)
        ''' Contains: Count of number topics in dataframe. '''
        self.headings = list(self.dataframe.columns.values)
        ''' Contains: List of dataframe column headers. '''
    def __str__(self):
        return lib.nice_print(self)


def factor_analysis(topics: int, method: str, rotation: str):
    ''' Returns: FactorAnalyzer result. '''
    return FactorAnalyzer(
            n_factors=topics, 
            method=method, 
            rotation=rotation
    )


class EFA_Factorability:
    ''' Purpose: Construct class storing EFA factorability results. '''
    def __init__(self, settings: EFA_Settings):
        bart = calculate_bartlett_sphericity(settings.dataframe)
        self.bartlett_chi_square_score = bart[0]
        ''' Contains: Barlett sphericity chi square score. ''' 
        self.bartlett_p_value = bart[1]
        ''' Contains: Barlett sphericity p value result. '''
        self.kmo_score = calculate_kmo(settings.dataframe)[1]
        ''' Contains: Kaiser-Meyer-Olkin test score. '''
    def __str__(self):
        return lib.nice_print(self)


def plot_eigen(eigenvalues: list, name: str, width: int):
    ''' Purpose: Creates visualisation of eigenvalue results. '''
    pylt.figure(figsize=(8, 6))
    pylt.axhline(y=1, c='k', linestyle='dashdot', alpha=0.4)
    pylt.scatter(range(1, width+1), eigenvalues, c='b')
    pylt.plot(range(1, width+1), eigenvalues, 'b', label='EFA - Data')
    pylt.xlabel('Factor', {'fontsize': 15})
    pylt.ylabel('Eigenvalue', {'fontsize': 15})
    pylt.legend()
    pylt.savefig(f'{lib.RESULTFOLDER}{name}_eigen_analysis.png')


def plot_scree(proportional_variance: list, name: str, width: int):
    ''' Purpose: Creates visualisation of variance explained by factor. '''
    pylt.figure(figsize=(8, 6))
    pylt.plot(range(1, width+1), proportional_variance,
              'o-', linewidth=2, color='blue', label='EFA - Data')
    pylt.xlabel('Factor', {'fontsize': 15})
    pylt.ylabel('Variance Explained', {'fontsize': 15})
    pylt.legend()
    pylt.savefig(f'{lib.RESULTFOLDER}{name}_variance_scree.png')


class EFA_Eigen:
    ''' Purpose: Build class of eigenvalue analysis results. '''
    def __init__(self, settings: EFA_Settings):
        efa = factor_analysis(settings.topics, settings.method, None)
        efa.fit(settings.dataframe)
        variance = efa.get_factor_variance()
        self.variance = variance[0]
        ''' Contains: List of variance results. '''
        self.proportional_variance = variance[1]
        ''' Contains: List of proportional variance results. '''
        self.cumulative_variance = variance[2]
        ''' Contains: List of cumulative variance results. '''
        self.eigenvalues = efa.get_eigenvalues()[0]
        ''' Contains: List of eigenvalue results from analysis. '''
        self.suggested = next(x[0] for x in enumerate(self.eigenvalues) if x[1] < 1)
        ''' Contains: Eigenvalue analysis based topics suggestion. '''
    def plot(self, name, number_topics):
        ''' Purpose: Saves plot of eigenvalue analysis results. '''
        plot_eigen(self.eigenvalues, name, number_topics)
    def scree(self, name, number_topics):
        ''' Purpose: Saves scree plot of variance explained. '''
        plot_scree(self.proportional_variance, name, number_topics)
    def __str__(self):
        return lib.nice_print(self)


def random_eigens(efa: FactorAnalyzer, dataframe, times: int = 100):
    ''' Purpose: Constructs random eigenvalue matrix for EFA. '''
    height, width = dataframe.shape
    sum_eigens = numpy.empty(width)
    for _ in range(times):
        efa.fit(numpy.random.normal(size=(height, width)))
        sum_eigens = sum_eigens + efa.get_eigenvalues()[0]
    return sum_eigens / times, efa


def plot_horn(eigenvalues: list, random_eigenvalues: list, name: str, width: int):
    ''' Purpose: Creates visualisation of horn parallel analysis results. '''
    pylt.figure(figsize=(8, 6))
    pylt.axhline(y=1, c='k', linestyle='dashdot', alpha=0.4)
    pylt.plot(range(1, width+1), random_eigenvalues, 'blue', label='EFA - random', alpha=0.4)
    pylt.scatter(range(1, width+1), eigenvalues, c='blue', marker='o')
    pylt.plot(range(1, width+1), eigenvalues, 'blue', label='EFA - data')
    pylt.xlabel('Factor', {'fontsize': 15})
    pylt.ylabel('Eigenvalue', {'fontsize': 15})
    pylt.legend()
    pylt.savefig(f'{lib.RESULTFOLDER}{name}_horn_analysis.png')


class EFA_Horn:
    ''' Purpose: Build class of horn analysis results. '''
    def __init__(self, settings: EFA_Settings):
        efa = factor_analysis(settings.topics - 1, settings.method, None)
        self.random_eigenvalues, efa = random_eigens(efa, settings.dataframe)
        ''' Contains: Generated random matrix of eigenvalues. '''
        efa.fit(settings.dataframe)
        self.eigenvalues = efa.get_eigenvalues()[0]
        self.suggested = sum((self.eigenvalues - self.random_eigenvalues) > 0)
        ''' Contains: Horn parallel analysis based topics suggestion. '''
    def plot(self, name, number_topics):
        plot_horn(self.eigenvalues, self.random_eigenvalues, name, number_topics)
    def __str__(self):
        return lib.nice_print(self)


def check_number(_, number: str):
    ''' Purpose: Validates number of topics input. '''
    if not number.isdigit():
        raise inquirer.errors.ValidationError('', reason = f'{number} is not a valid number...')
    return True


def get_topics():
    ''' Returns: User entered number of topics. '''
    print('')
    return int(inquirer.text(
                message = 'Please select a number of topics',
                validate = check_number
    ))


def base26(n):
    ''' Returns: Base26 representation of integer. '''
    a = ''
    while n:
        m = n % 26
        if m > 0:
            n //= 26
            a += chr(64 + m)
        else:
            n = n // 26 - 1
            a += 'Z'
    return a[::-1]


def plot_efa(loadings, name: str, number_topics: int, headers: list):
    ''' Purpose: Creates visualisation of EFA results. '''
    grid = numpy.abs(loadings)
    xlabels = [f'Factor {base26(x + 1)}' for x in range(number_topics)]
    figure, axis = pylt.subplots()
    x = axis.pcolor(grid, cmap='Blues')
    figure.colorbar(x, ax=axis)
    axis.set_yticks(numpy.arange(loadings.shape[0])+0.5, minor=False)
    axis.set_xticks(numpy.arange(loadings.shape[1])+0.5, minor=False)
    axis.set_yticklabels(headers)
    axis.set_xticklabels(xlabels)
    figure.tight_layout()
    pylt.savefig(f'{lib.RESULTFOLDER}{name}_EFA.png')


class EFA:
    ''' Purpose: Construct class storing EFA results. '''
    def __init__(self, settings: EFA_Settings, number_topics: int):
        self.topics = number_topics
        ''' Contains: User specified number of topics for EFA. '''
        efa = FactorAnalyzer(method=settings.method)
        efa.set_params(n_factors=number_topics, rotation=settings.rotation)
        efa.fit(settings.dataframe)
        self.loadings = efa.loadings_
        ''' Contains: List of factor loading results. '''
        self.communality = efa.get_communalities()
        ''' Contains: List of communality results. '''
        self.uniqueness = efa.get_uniquenesses()
        ''' Contains: List of uniqueness results. '''
    def plot(self, name, number_topics, headings):
        plot_efa(self.loadings, name, number_topics, headings)
    def __str__(self):
        return lib.nice_print(self)


def check_filename(_, text: str):
    ''' Purpose: Validates filename has acceptable characters and does not exist. '''
    if not re.match(r'^[A-Za-z0-9_-]*$', text):
        raise inquirer.errors.ValidationError('', reason = f'{text} contains invalid characters...')
    existing = lib.get_files(lib.RESULTFOLDER, '.txt')
    if f'{text}.txt' in existing:
        raise inquirer.errors.ValidationError('', reason = f'{text} is an existing result name...')
    return True


def get_name():
    ''' Returns: User entered result name. '''
    return inquirer.text(
        message = 'Please enter a name for results',
        validate = check_filename
    )


def save_results(name: str, settings: EFA_Settings, factorability: EFA_Factorability,
                 eigens: EFA_Eigen, horn: EFA_Horn, result: EFA):
    ''' Purpose: Saves all relevant figures and text results for EFA. '''
    eigens.plot(name, settings.topics)
    eigens.scree(name, settings.topics)
    horn.plot(name, settings.topics)
    result.plot(name, result.topics, settings.headings)
    with open(f'{lib.RESULTFOLDER}{name}.txt', 'a') as output:
        output.write(f'SETTINGS\n\n{str(settings)}\n\n')
        output.write(f'FACTORABILITY\n\n{str(factorability)}\n\n')
        output.write(f'EIGEN VALUE ANALYSIS\n\n{str(eigens)}\n\n')
        output.write(f'HORN PARALLEL ANALYSIS\n\n{str(horn)}\n\n')
        output.write(f'EFA RESULTS\n\n{str(result)}\n\n')


def efa_analysis():
    try:
        efa_settings = EFA_Settings()
        print(lib.Formats.status(f'Calculating data factorability'))
        efa_factorability = EFA_Factorability(efa_settings)
        print(lib.Formats.status(f'Performing eigenvalue analysis'))
        efa_eigens = EFA_Eigen(efa_settings)
        print(lib.Formats.info(f'Suggested topics: {efa_eigens.suggested}'))
        print(lib.Formats.status(f'Performing horn parallel analysis'))
        efa_horn = EFA_Horn(efa_settings)
        print(lib.Formats.info(f'Suggested topics: {efa_horn.suggested}'))
        number_topics = get_topics()
        print(lib.Formats.status(f'Performing the defined EFA'))
        efa_results = EFA(efa_settings, number_topics)
        name = get_name()
        save_results(name, efa_settings, efa_factorability, efa_eigens, efa_horn, efa_results)
    except Exception as error:
       print(lib.Formats.alert(f'EFA analysis failed:\n{error}'))
       quit()


if __name__ == '__main__':
    efa_analysis()
