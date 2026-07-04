import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate panel-thuhoi
start_thuhoi = html.find('<div class="main-panel" id="panel-thuhoi">')
if start_thuhoi != -1:
    end_thuhoi = html.find('</div>\n</div>\n<div class="table-wrap"', start_thuhoi)
    if end_thuhoi != -1:
        panel_html = html[start_thuhoi:end_thuhoi]
        
        # We need to find the specific pattern:
        # </div>
        #         <div class="filter-row" style="margin-bottom: 0; justify-content: flex-end;">
        # Because line 701 is </div> and line 702 is <div class="filter-row"...
        
        # The filter-row ends with:
        # <label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-basket="B0017" data-warehouse="Rau" onchange="toggleBasketCheck('B0017',this)">Tote đỏ bánh tươi</label>
        # </div>
        #             </div>
        #         </div>
        #         <div class="filter-group">
        
        # Let's use regex to find the misplaced </div>
        # It's right after <!-- CAL_GRID_END -->\n            </div>\n        </div>\n    </div>
        
        # We want to replace:
        #             </div>
        #         </div>
        #     </div>
        #         <div class="filter-row" style="margin-bottom: 0; justify-content: flex-end;">
        # With:
        #             </div>
        #         </div>
        #         <div class="filter-row" style="margin-bottom: 0; justify-content: flex-end;">
        
        old_pattern = r'            </div>\n        </div>\n    </div>\n        <div class="filter-row"'
        new_pattern = r'            </div>\n        </div>\n        <div class="filter-row"'
        
        if re.search(old_pattern, panel_html):
            panel_html = re.sub(old_pattern, new_pattern, panel_html)
            
            # Now we need to ADD the </div> back at the end of the filter-row block!
            # The filter-row block ends around the "Tìm kiếm" filter group:
            #             </div>
            #         </div>
            #     </div>
            #         <div class="color-legend" style="margin-bottom: 0;">
            
            # So we look for:
            #                 <button class="search-clear" onclick="clearSearch('trip-store-search','filterTripStore')">&times;</button>
            #             </div>
            #         </div>
            #     </div>
            #         <div class="color-legend"
            
            end_pattern = r'            </div>\n        </div>\n    </div>\n        <div class="color-legend"'
            new_end_pattern = r'            </div>\n        </div>\n    </div>\n    </div>\n        <div class="color-legend"'
            
            if re.search(end_pattern, panel_html):
                panel_html = re.sub(end_pattern, new_end_pattern, panel_html)
                
                html = html[:start_thuhoi] + panel_html + html[end_thuhoi:]
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print("Fixed panel-thuhoi layout")
            else:
                print("Could not find end of filter-row")
        else:
            print("Could not find start of filter-row")
