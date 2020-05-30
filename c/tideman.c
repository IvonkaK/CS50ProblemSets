#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool check_cycles(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    //first iteration checks the ith candidate in ranks array
    for (int i = 0; i < candidate_count; i++)
    {
        //inner checks ith + 1 candidate in ranks array
        for (int j = i + 1; j < candidate_count; j++)
        {
            //record one vote for leading candidates in ranks (last candidate in ranks array has no votes over any previous candidates)
            preferences[ranks[i]][ranks[j]] ++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            //compare each pair once and save both candidates from pair to pairs[] as winner/loser
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count ++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count ++;
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    //iterate through preferences 2d array and check the number of votes (strength) between pairs of candidates
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            // compare the number of votes in pref array of candidates
            if (preferences[pairs[j].winner][pairs[j].loser] < preferences[pairs[j + 1].winner][pairs[j + 1].loser])
            {
                //swap their order in pair struct to place the pair with highest score as first
                pair temp = pairs[j + 1];
                pairs[j + 1] = pairs[j];
                pairs[j] = temp;
            }
        }
    }
}

//helper function to check for cycles in graph
bool check_cycles(int winner, int loser)
{
    //return true if the position of current loser to winer is locked
    if (locked[loser][winner] == true)
    {
        return true;
    }

    //iterate candidates and check if position of current loser [i] is true
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i] == true)
        {
            //if above is true check the cycle again between current winner and i (i is the loser of the previously checked pair)
            return check_cycles(winner, i);
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        //use check_cycle helper to determine if the pair can be locked
        if (check_cycles(pairs[i].winner, pairs[i].loser) == false)
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    int count;
    
    for (int row = 0; row < candidate_count; row++)
    {
        count = 0;
        
        for (int column = 0; column < candidate_count; column++)
        {
            if (locked[column][row] == false)
            {
                count ++;
            }
        }
        
        //if the number of counted 'false' edges from the graph is as high as the number of candidates that candidate with position[row] is the source
        if (count == candidate_count)
        {
            printf("%s\n", candidates[row]);
        }
    }
}

