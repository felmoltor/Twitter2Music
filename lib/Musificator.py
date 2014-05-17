class Musificator:

    def __init__(self):
        # http://www.phy.mtu.edu/~suits/notefreqs.html
        # Using A4 frecuencies        
        self.freqtable = {
            "C": 261.63,
            "C#": 277.18,
            "D": 293.66,
            "D#": 311.13,
            "E": 329.63,
            "F": 349.23,
            "F#": 369.99,
            "G": 392.00,
            "G#": 415.30,
            "A": 440.00,
            "A#": 466.16,
            "B": 493.88
        }
        self.quaverduration = 0.2
        self.crotchetduration  = self.quaverduration * 2.0
        self.minimduration = self.crotchetduration * 2.0
        self.semibreveduration = self.crotchetduration * 2.0
        self.silentime = 1.0
        self.msg = ""
        self.frequencies = []
        self.durations = []

    def musificate(self, message = ""):
        """
        This function translates a string of letters to frecuencies and durations.
        The frecuency is determined by the name of the note ABCDEFG (# http://www.phy.mtu.edu/~suits/notefreqs.html)
        The duration is determined by the case of the letter or other symbol "_":
            * Low case: is a quaver note
            * Up case: is a crotchet note
            * Low case with a dash: "-": Is a minim note
            * Up case with a dash: "-": Is a semibreve note
        """
        self.msg = message        
        freqs = []
        durations = []
        count = 0
        note = ""
        
        print "Musificando el mensaje '%s', de longitud %s" % (message,len(message))
        while count < len(message):
            note = message[count]
            
            # Check if is in our note aplphabet
            if note.upper() not in self.freqtable:
                return freqs,durations
            else:
                # Explore de duration of the note            
                if note.isupper():
                    if message[(count+1)%len(message)] == "-":
                        durations.append(self.semibreveduration)
                        count += 1
                    else:
                        durations.append(self.minimduration)
                    
                else:
                    if message[(count+1)%len(message)] == "-":
                        durations.append(self.crotchetduration)
                        count += 1
                    else:
                        durations.append(self.quaverduration)
                
                # Is a half tone upper (#)
                if message[(count+1)%len(message)] == "#":
                    note += "#"
                    count += 1                
                freqs.append(self.freqtable[note.upper()])
                
            count += 1
        self.frequencies = freqs
        self.durations = durations
        
        return self.frequencies, self.durations
    
    def demorsificate(self, morsecode = ""):
        self.msg = ""
        self.translatedmsg = morsecode
        self.msg = "<NOT IMPLEMENTED>"
        return self.msg
        
        