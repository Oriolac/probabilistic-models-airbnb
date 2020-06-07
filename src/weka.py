def categorize(dataframe, column, number_divisions, cat_func):
    """
        Changes a column of a Dataframe categorizing its data.
        :param dataframe: pandas.Dataframe -> Dataframe to be categorized
        :param column: column name of the header, column that must be categorized
        :param number_divisions: Length of the set range of divisions
        :param cat_func: partition function that has to return a column of categorized data.
        :return:
    """
    dataframe[column] = cat_func(dataframe[column],
                                 number_divisions, labels=False)


def parse_weka(df, relation_name, seed):
    """
        Parses a pandas.DataFrame to weka format, independently
        from the weka format. All attributes must be categorized
        before this function.
        It's a pure function.

        :param df: pandas.DataFrame -> DataFrame to be parsed.
        :param relation_name: str -> relation name used in weka.
        Its the first line containing:
         `@RELATION {relation_name}`

        :return string with weka format-like. With this it's
        straight-forward to save it in a file.
    """

    prefix = create_prefix(df, relation_name)
    train = get_training(df, seed)
    test = get_test(df, train)
    return sample_arff(prefix, train), sample_arff(prefix, test)


def sample_arff(prefix, sample):
    """
    Creates the str of an ARFF file whith the relation information and its data.
    :param prefix: str which has to be at the beginning of the file
    :param sample: A Dataframe that can be the training set or the test set.
    :return: str which has to be in the ARFF file.
    """
    res = prefix + '\n\n@DATA\n'
    res += '\n'.join(','.join(f"'{str(x)}'" for x in row)
                     for row in sample.values)
    return res


def create_prefix(df, relation_name):
    """
    Creates the prefix of the dataset: name of the relation and all of the atributes.
    :param df: Dataset
    :param relation_name: Name of the relation
    :return: The prefix str which must be at the beginning of the ARFF file.
    """
    prefix = f"@RELATION {relation_name}\n\n"
    prefix += '\n'.join(f'@ATTRIBUTE {col} ' + '{' +
                        ','.join(f"'{str(x)}'" for x in df[col].unique())
                        + '}' for col in df.columns)
    return prefix


def get_test(df, train):
    """
    Get the Dataframe Test
    :param df: Dataframe which has all the dataset, the training and test data.
    :param train: Dataframe which has the training dataset.
    :return: Dataframe difference from the training and all the dataset.
    """
    return df.drop(train.index)


def get_training(df, seed):
    """
    Return a DataFrame which contains the training set.
    :param df: Dataframe which has all the dataset, the training and test data.
    :param seed: Used for randomly split the Dataframe df for a seed
    :return: the training Dataframe
    """
    return df.sample(frac=0.75, random_state=seed)
