import Conversations
Conversations.manage_characters()














#
#
#UserNumInput = input("How many characters? [1] ")
#UserSeedInput = input("Seed character? [Medieval] ")
#
## Check if user provided input for Num and convert it to an integer if they did
#UserNum = int(UserNumInput) if UserNumInput else None
#UserSeed = UserSeedInput if UserSeedInput else None
#
## Call the function with the appropriate arguments
#if UserNum is not None and UserSeed is not None:
#    idea = Conversations.imagine_character(Num=UserNum, Seed=UserSeed)
#elif UserNum is not None:
#    idea = Conversations.imagine_character(Num=UserNum)
#elif UserSeed is not None:
#    idea = Conversations.imagine_character(Seed=UserSeed)
#else:
#    idea = Conversations.imagine_character()
#
#
#print(idea)
#Continue = input("Continue?[n/y] ")
#if Continue == "y":
#    char = Conversations.create_character(idea)
#    print("--------------------")
#    print(Conversations.summarize_character(char))
#    print("--------------------")
#    print(char)
##start_chat("""You are an AI Actor in a videogame portraying characters that are sent to you. You will produce dialog on behalf of the character.""")
##description = input("Enter Description: ")
##character = create_character(description)
##summary = summarize_character(character)
##print(summary)