
class ItemExtractor:
    """
    This class is designed to be an iterator that iterates over some items presented by Jira.
    """

    def __init__(self, connection, connection_string, provider, batch_size=10):
        """
        Initializes an iterator for retrieving a Jira resource with pagination.

        This initializes an iterator that provides resources in batches based on the resource defined by the connection string and values provided in the provider function.

        Parameters
        ----------
        connection : Connection
            Connection object to be used to retrieve the resources from Jira.
        connection_string : String
            This is the string that is passed as a custom Request to retrieve resources. Values that depend on the object must be formatted in and passed in with the provider function.
        provider : Lambda
            This is a lambda that takes in no arguments and returns a tuple (with any number of values) that contain the arguments to be formatted into the connection_string.
        batch_size : Integer (Optional)
            This is an optional argument that sets the batch size for retrieval.

        Returns
        -------
        Nothing

        """

        self.start_at_marker = 0
        self.connection_string = connection_string
        self.connection = connection
        self.provider = provider
        self.batch_size = batch_size

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns the next batch of resources from Jira.

        Takes the start position, and returns the next <batch_size> resources from Jira through the connection. If no more exist, will continue to increment self.start_at_marker, so it's not safe to call continuously until new resources appear in Jira.

        Parameters
        ----------
        None

        Returns
        -------
        String
            JSON String returned by the connection

        """

        request_string = (self.connection_string + "&startAt=%d&maxResults=%d") % (self.provider() + (self.start_at_marker, self.batch_size))
        resources_response = self.connection.customRequest(request_string).json()
        #print(resources_response)
        self.start_at_marker = resources_response["startAt"]
        return resources_response

    @staticmethod
    def create_column_issue_extractor(board, column, batch_size=10):
        """
        Create an ItemExtractor that extracts only items from one column.

        Create an ItemExtractor that creates an extractor only for statuses associated with a specific column of a board.

        Parameters
        ----------
        board : Board
            The board object from which we are extracting the issues
        column : String
            The column name of the column to be extracted
        batch_size : Integer (Optional)
            Optional batch size

        Returns
        -------
        ItemExtractor
            ItemExtractor instance that gets issues from this particular column

        """

        #print([k for k, v in board.statusToColumn.items() if v == column])
        return ItemExtractor(board.connection, board.baseUrl+"/issue?fields=%s&jql=status IN (%s)", lambda: (','.join(board.requiredProperties), ','.join(['\'%s\'' % k for k, v in board.statusToColumn.items() if v == column])), batch_size)

