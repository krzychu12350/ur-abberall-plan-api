import shutil

from pydub import AudioSegment

'''
1. Loudness
from pydub import AudioSegment
sound1 = AudioSegment.from_file("sound1.wav")

# make sound1 louder by 3.5 dB
louder_via_method = sound1.apply_gain(+3.5)
louder_via_operator = sound1 + 3.5

# make sound1 quieter by 5.7 dB
quieter_via_method = sound1.apply_gain(-5.7)
quieter_via_operator = sound1 - 5.7
'''


class Mixer:
    def mergeFiles(self):
        clap = AudioSegment.from_wav("sounds/clap.wav")
        # play(song)

        fill = AudioSegment.from_wav("sounds/fill.wav")

        impact = AudioSegment.from_wav("sounds/impact.wav")

        # with_style = fill.append(clap, crossfade=100)
        #
        # three_concat = with_style.append(impact, crossfade=2000)

        # play(clap + fill + impact)
        awesome = clap + fill + impact
        file_path = "./mashup.mp3"
        awesome.export(file_path, format="mp3", bitrate="192k")

        return file_path
        # play(three_concat)

    def convertMilisecondsToMinuteSecondFormat(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        return "%d:%d:%d" % (hours, minutes, seconds)

    def saveFileFromRequestOnDisk(self, file):
        file_location = f"./request-files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

    def addFadeInToAudioFile(self, filePath, duration):
        file = AudioSegment.from_mp3(filePath)
        return file.fade_in(duration)

    def addFadeOutToAudioFile(self, filePath, duration):
        file = AudioSegment.from_wav(filePath)
        return file.fade_out(duration)

    def mixFileSounds(self, files, instrumental):
        global file_path, mix
        self.saveFileFromRequestOnDisk(instrumental)

        for f in files:
            self.saveFileFromRequestOnDisk(f)

        file_names_list = []
        for file in files:
            file_names_list.append('request-files/' + file.filename)

        instrumental_path = 'request-files/' + instrumental.filename
        print("files")
        print(file_names_list)
        print("instrumental")
        print(instrumental_path)
        #  Zaczyna się od podkładu, fade-in 2 sekundy.

        fade_in_instrumental = self.addFadeInToAudioFile(instrumental_path, 2000)
        fade_in_instrumental.export(instrumental_path, format="wav")

        '''
        Zaczyna się od podkładu, fade-in 2 sekundy.
        Po 5 sekundach 1 plik mp3 (podkład jest cały czas)
        każdy następny plik mp3 odtwarza się po 10 sekundach od zakończenia poprzedniego.
        po ostatnim pliku 10s i 3s fade-out.
        '''
        # instrumental = AudioSegment.from_mp3(instrumental_path)
        mix_position = 5000
        counter = 1
        final_mix_version = ''

        for file in file_names_list:
            file_to_mix = AudioSegment.from_wav(file)
            print(file)
            partial_mix_path_to_export = 'output-mixes/mix_' + str(counter) + '.wav'
            previous_mix_partial = 'output-mixes/mix_' + str(counter - 1) + '.wav'
            if counter == 1:
                current_instrumental = AudioSegment.from_wav(instrumental_path)
            else:
                current_instrumental = AudioSegment.from_wav(previous_mix_partial)
            print(partial_mix_path_to_export )
            mix = current_instrumental.overlay(file_to_mix, position=mix_position)

            duration_millis = round(file_to_mix.duration_seconds  * 1000)
            #print(str(duration_millis))

            print("Sample duration: " + str(self.convertMilisecondsToMinuteSecondFormat(duration_millis)))
            print("Current sample position: " + str(self.convertMilisecondsToMinuteSecondFormat(mix_position)))

            print("Counter: " + str(counter))
            file_path = "./output-mixes/mix_" + str(counter) + ".wav"
            mix.export(partial_mix_path_to_export, format="wav")
            final_mix_version = partial_mix_path_to_export

            current_position = duration_millis + 10000
            mix_position += current_position
            counter += 1

        # file_to_mix = AudioSegment.from_wav(file_names_list[1])
        # instrumental_2 = AudioSegment.from_mp3(file_path)
        # mix = fade_in_instrumental.overlay(file_to_mix, position=mix_position)
        # print("Mix position: " + str(mix_position))
        # file_path = "./output-mixes/mix_" + str(counter) + ".wav"
        # mix.export(file_path, format="wav")
        # mix_position += 10000
        # counter += 1






        # E:\FlStudioVSTLargeSize\Sample\kshmr.vol.4\Vocals\Vocal Tools\Vocal Bends
        # print(file_location)
        # # Zaczyna się od podkładu, fade-in 2 sekundy.
        # instrumental_fade_in = contents.fade_in(2000)
        #
        # fill = AudioSegment.from_wav("./sounds/fill.wav")
        #
        # #Po 5 sekundach 1 plik mp3 (podkład jest cały czas)
        #  mix =  instrumental_fade_in.overlay(fill, position=5000)
        # file_path = "./output-mix.mp3"
        # mix.export(file_path, format="mp3")

       # return file_path

        fade_out_path = './output-mixes/last.wav'
        fade_out = self.addFadeOutToAudioFile(final_mix_version, 10000)
        fade_out.export(fade_out_path, format="wav")

        return fade_out_path
      #  return final_mix_version
