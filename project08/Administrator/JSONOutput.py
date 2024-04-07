from AutomatedGamePlay import AutomatedGamePlay

class JSONOutput:
    def __init__(self) -> None:
        self.share_count= {
            "Worldwide": 0,
            "Sackson": 0,
            "Festival": 0,
            "Imperial": 0,
            "American": 0,
            "Continental": 0,
            "Tower": 0,
        }
    
    def runGame(self,input_data):
        self.automatedGame=AutomatedGamePlay(state=input_data,test_mode=True)
        res=self.automatedGame.orderedStrategy()
        output=self.automatedGame.game.getStateObj()
        return self.compareJSON(input_data,output,res)

    def compareJSON(self,input_data,output,res):
        initial_shares=input_data["player"][0]["shares"]
        initial_tiles=set()
        for tile in input_data["player"][0]["tiles"]:
            initial_tiles.add((tile["row"],tile["column"]))
        final_shares=output["players"][-1]["shares"]
        final_tiles=set()
        for tile in output["players"][-1]["tiles"]:
            final_tiles.add((tile["row"],tile["column"]))

        if initial_tiles==final_tiles:
            return self.getActionObj(res,None,None,[])

        placed_tile_list=list(initial_tiles.difference(final_tiles))

        for share in initial_shares:
            self.share_count[share["share"]]+=share["count"]

        bought_share=[]
        for share in final_shares:
            start=self.share_count[share["label"]]
            if start<share["count"]:
                num=share["count"]-start
                for i in range(0,num):
                    bought_share.append(share["label"])
        
        
        return self.getActionObj(res,placed_tile_list[0][0],placed_tile_list[0][1],bought_share)
    
    def getActionObj(self,res,row,col,bought):
        print(row,col)
        win_state=True if res else False
        if not row or not col:
            return {"win": win_state,"hotel":bought}
        hotel=self.automatedGame.game.board.board[int(ord(row)-ord("A"))][int(col) - 1]
        if hotel not in (" ","O"):
            return {"win": win_state,"hotel":bought,"place":{"row":row,"column":col,"hotel":hotel}}
        else:
            return {"win": win_state,"hotel":bought,"place":{"row":row,"column":col}}
