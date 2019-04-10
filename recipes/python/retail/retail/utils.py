#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2017 Adobe
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.
#####################################################################


class Utils:


    def mapFields(self, configProperties={}, dataframe=None):

        tenantId = configProperties.get("tenantId")
        # Rename columns
        dataframe = dataframe.rename({tenantId+'.cpi':'cpi', tenantId+'.date':'date', tenantId+'.isHoliday':'isHoliday', tenantId+'.markdown':'markdown',
                                      tenantId+'.regionalFuelPrice':'regionalFuelPrice', tenantId+'.store':'store', tenantId+'.storeSize':'storeSize',
                                      tenantId+'.storeType':'storeType', tenantId+'.temperature':'temperature', tenantId+'.unemployment':'unemployment',
                                      tenantId+'.weeklySales':'weeklySales'}, axis='columns')

        #Drop id, eventType and timestamp
        dataframe.drop(['_id', 'eventType', 'timestamp'], axis=1, inplace=True)

        return dataframe

