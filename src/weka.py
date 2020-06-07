
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

    def sample_arff(prefix, sample):
        res = prefix + '\n\n@DATA\n'
        res += '\n'.join(','.join(f"'{str(x)}'" for x in row)
                         for row in sample.values)
        return res

    prefix = f"@RELATION {relation_name}\n\n"

    prefix += '\n'.join(f'@ATTRIBUTE {col} ' + '{' +
                        ','.join(f"'{str(x)}'" for x in df[col].unique())
                        + '}' for col in df.columns)
    train = df.sample(frac=0.75, random_state=seed)
    test = df.drop(train.index)
    return sample_arff(prefix, train), sample_arff(prefix, test)
