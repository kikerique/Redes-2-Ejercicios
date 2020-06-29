# Copy your GreedyMotifSearch function (along with all required subroutines) from Motifs.py below this line

class MotifsSearcher:
    def Profile(self,Motifs):
        t = len(Motifs)
        k = len(Motifs[0])
        profile = self.Count(Motifs)
        for c in "ACGT":
            for i in range(k):
                profile[c][i]=profile[c][i]/t
        # insert your code here
        return profile
    def Consensus(self,Motifs):
        # insert your code here
        countMatrix=self.Count(Motifs)
        consensus=""
        for i in range(len(Motifs[0])):
            a1="A" if countMatrix["A"][i]>countMatrix["C"][i] else "C"
            a2="G" if countMatrix["G"][i]>countMatrix["T"][i] else "T"
            consensus+=a1 if(countMatrix[a1][i]>countMatrix[a2][i]) else a2
        return consensus
    # Copy your Count(Motifs) function here.
    def Count(self,Motifs):
        count = {}
        for c in "ACGT":
            count[c]=[0]*len(Motifs[0])
        for i in range(len(Motifs)):
            for j in range(len(Motifs[i])):
                count[Motifs[i][j]][j]+=1
        return count
    # Input:  A set of k-mers Motifs
    # Output: The score of these k-mers.
    def Score(self,Motifs):
        # Insert code here
        k=len(Motifs)
        consensus=self.Consensus(Motifs)
        count=self.Count(Motifs)
        score=0
        for i in range(len(consensus)):
            score+=k-count[consensus[i]][i]
        return score
    # Then copy your ProfileMostProbableKmer(Text, k, Profile) and Pr(Text, Profile) functions here.
    def Pr(self,Text, Profile):
        probability=1
        # insert your code here
        for i in range(len(Text)):
            probability*=Profile[Text[i]][i]
        return probability

    def ProfileMostProbableKmer(self,text, k, profile):
        mostProbableProfile=text[0:k]
        probability=0
        for i in range (len(text)-k+1):
            probe=text[i:i+k]
            test=self.Pr(probe,profile)
            if probability<test:
                probability=test
                mostProbableProfile=probe
        return mostProbableProfile
    # Input:  A list of kmers Dna, and integers k and t (where t is the number of kmers in Dna)
    # Output: GreedyMotifSearch(Dna, k, t)
    def GreedyMotifSearch(self,Dna, k, t):
        # type your GreedyMotifSearch code here.
        BestMotifs = []
        for i in range(0, t):
            BestMotifs.append(Dna[i][0:k])
        n = len(Dna[0])
        for i in range(n-k+1):
            Motifs = []
            Motifs.append(Dna[0][i:i+k])
            for j in range(1, t):
                P = self.Profile(Motifs[0:j])
                Motifs.append(self.ProfileMostProbableKmer(Dna[j], k, P))
            if self.Score(Motifs) < self.Score(BestMotifs):
                BestMotifs = Motifs
        return BestMotifs
    # Copy the ten strings occurring in the hyperlinked DosR dataset below.
    # set t equal to the number of strings in Dna and k equal to 15
    """t=len(Dna)
    k=15
    # Call GreedyMotifSearch(Dna, k, t) and store the output in a variable called Motifs
    Motifs=GreedyMotifSearch(Dna, k, t)
    # Print the Motifs variable
    print(Motifs)
    # Print Score(Motifs)
    print(Score(Motifs))"""